from typing import List, Callable, NamedTuple

from wwwpy import HttpResponse
from wwwpy.http_request import Request


class Route(NamedTuple):
    path: str
    callback: Callable[[Request], HttpResponse]


class Routes:
    def __init__(self):
        self.list: List[Route] = []

    def add_route(self, path: str, callback: Callable[[Request], HttpResponse]) -> 'Routes':
        self.list.append(Route(path, callback))
        return self

    def add_route_obj(self, route: Route) -> 'Routes':
        self.list.append(route)
        return self

    @property
    def is_empty(self) -> bool:
        return len(self.list) == 0
