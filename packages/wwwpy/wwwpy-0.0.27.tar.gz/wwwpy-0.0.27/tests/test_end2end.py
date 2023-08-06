from pathlib import Path

from playwright.sync_api import Page, expect

from tests import for_all_webservers, new_config
from wwwpy import Webserver


@for_all_webservers()
def test_quickstart_bootstrap(page: Page, webserver: Webserver):
    config = new_config(webserver)
    config.bootstrap.add_python(
        """print('running bootstrap custom code')\n"""
        """from js import document\n"""
        """document.body.innerHTML='<input id="tag1" value="Hello world 1!">'\n"""
        """print(f'document.body.innerHTML=[{document.body.innerHTML}]')\n"""
    )
    page.goto(config.webserver.localhost_url())
    expect(page.locator('id=tag1')).to_have_value('Hello world 1!')


@for_all_webservers()
def test_bootstrap_bundle(page: Page, webserver: Webserver):
    config = new_config(webserver)
    config.bundles.add_file_content(
        'script1.py',
        """from js import document\n"""
        """document.body.innerHTML='<input id="tag1" value="Hello world 2!">'\n"""
    )
    config.bootstrap.add_python('import script1')

    page.goto(config.webserver.localhost_url())
    expect(page.locator('id=tag1')).to_have_value('Hello world 2!')


@for_all_webservers()
def test_bootstrap_bundle_from_filesystem(page: Page, webserver: Webserver):
    config = new_config(webserver)
    config.bundles.add_flat_folder(Path(__file__).parent / 'data' / 'for_remote')
    config.bootstrap.add_python('import main')

    page.goto(config.webserver.localhost_url())
    expect(page.locator('id=tag1')).to_have_value('Hello world 3!')
