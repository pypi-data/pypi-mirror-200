from __future__ import annotations

import sys
import traceback
from pathlib import Path
from types import ModuleType
from typing import Optional, Iterator

from wwwpy import Bundles
from wwwpy.bootstrap import Bootstrap
from wwwpy.http_request import Request
from wwwpy.http_response import HttpResponse
from wwwpy.resources import Resource, PathResource, stacktrace_pathfinder
from wwwpy.routes import Routes
from wwwpy.rpc import Services, Stubber, Module
from wwwpy.webserver import Webserver
from wwwpy.webserver import wait_forever
from wwwpy.webservers.available_webservers import available_webservers


class Config:
    def __init__(self):
        self._routes = Routes()
        self.bootstrap = Bootstrap()
        self.bundles = Bundles()
        self._webserver: Optional[Webserver] = None
        self.bundle_route = '/wwwpy/bundle/default.zip'

    @property
    def webserver(self) -> Webserver:
        if self._webserver is None:
            self._webserver = available_webservers().new_instance()
        return self._webserver

    def set_routes(self, routes: Routes) -> 'Config':
        if not self._routes.is_empty:
            raise Exception('routes are already set')
        self._error_if_attached()
        self._routes = routes
        return self

    def quickstart(
            self,
            blocking: bool = True,
            webserver_instance: Optional[Webserver] = None,
            port: Optional[int] = None,
            stack_backtrack=1,
            rpc_module: ModuleType = None,
            user_dir: str | None = None
    ) -> 'Config':
        if rpc_module is None:
            try:
                import server.rpc
                rpc_module = server.rpc
            except:
                traceback.print_exc()

        services = Services()
        if rpc_module is not None:
            rpc_module = Module(rpc_module)
            services.add_module(rpc_module)

        self.set_routes(
            Routes()
            .add_route(self.bundle_route, self.bundles.to_response)
            .add_route('/', self.quickstart_index_response)
            .add_route_obj(services.route)
        )

        if webserver_instance is None:
            webserver_instance = available_webservers().new_instance()
        if port is not None:
            webserver_instance.set_port(port)
        rpc_url = services.route.path
        stubber = Stubber(rpc_url, services, rpc_module)

        # one should be able to import:
        # - through an 'import module_name'
        # - through ??
        ef = user_dir
        if ef is None:
            ef = stacktrace_pathfinder(stack_backtrack)
        print(f'detected user dir: {ef}')
        print(f'{sys.path}')
        if ef is not None:
            self.bundles.add_flat_folder(ef.parent / 'app', relative_to=ef.parent)
            self.bundles.add_flat_folder(ef.parent / 'remote', relative_to=ef.parent)
            self.bundles.add_flat_folder(ef.parent / 'common', relative_to=ef.parent)
            remotepy = ef.parent / 'remote.py'

            def gen_remotepy() -> Iterator[Resource]:
                if remotepy.exists():
                    yield PathResource('remote.py', remotepy)
                yield from stubber.remote_stub_resources()

            self.bundles.add_resources(gen_remotepy)

        wwwpy_remote = Path(__file__).parent
        self.bundles.add_flat_folder(wwwpy_remote, relative_to=wwwpy_remote.parent)
        # language=python
        load_default_bundle = f"""
import sys
from pyodide.http import pyfetch
response = await pyfetch('{self.bundle_route}')
await response.unpack_archive(extract_dir='/default_bundle')
sys.path.insert(0, '/default_bundle')
"""
        self.bootstrap.add_python(load_default_bundle)
        # language=python
        self.bootstrap.add_python("""
import remote
await remote.main()
""")

        self.attach_webserver(webserver_instance)
        self.webserver.start_listen()

        if blocking:
            wait_forever()
        else:
            self.webserver.wait_ready()

        return self

    def quickstart_index_response(self, request: Request) -> HttpResponse:
        bootstrap_javascript = self.bootstrap.get_javascript()
        return HttpResponse(
            f'<h1>loading...</h1>'
            f'<script>{bootstrap_javascript}</script>'
            , 'text/html'
        )

    def attach_webserver(self, webserver: Webserver) -> 'Config':
        self._error_if_attached()
        self._webserver = webserver
        webserver.set_routes(self._routes)
        return self

    def _error_if_attached(self):
        if self._webserver is not None:
            raise Exception('Webserver already attached')
