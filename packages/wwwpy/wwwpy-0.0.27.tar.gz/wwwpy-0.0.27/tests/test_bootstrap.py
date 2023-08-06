from playwright.sync_api import Page, expect

import wwwpy
from tests import for_all_webservers
from wwwpy import Bootstrap, HttpResponse, Routes, Webserver
from wwwpy.server import find_port


@for_all_webservers()
def test_bootstrap(page: Page, webserver: Webserver):
    bootstrap_javascript = Bootstrap().add_python(
        'from js import document\n' +
        'document.getElementById("tag1").value = "Hello world!"\n'
    ).get_javascript()

    response = HttpResponse(f'<input id="tag1" value="Hello">'
                            f'<script>{bootstrap_javascript}</script>', 'text/html')

    routes = Routes().add_route('/', lambda _: response)
    webserver.set_routes(routes).set_port(find_port()).start_listen().wait_ready()

    page.goto(webserver.localhost_url())

    expect(page.locator('id=tag1')).to_have_value('Hello world!')


@for_all_webservers()
def test_bootstrap_config(page: Page, webserver: Webserver):
    cfg = wwwpy.Config()
    cfg.bootstrap.add_python(
        'from js import document\n' +
        'document.getElementById("tag1").innerHTML = "Hello bootstrap!"\n'
    )

    cfg.set_routes(Routes().add_route(
        '/',
        lambda _: HttpResponse(f'<div id="tag1"></div>'
                               f'<script>{cfg.bootstrap.get_javascript()}</script>', 'text/html')
    ))

    cfg.attach_webserver(webserver)
    webserver.set_port(find_port()).start_listen().wait_ready()

    page.goto(webserver.localhost_url())
    expect(page.locator('id=tag1')).to_have_text('Hello bootstrap!')
