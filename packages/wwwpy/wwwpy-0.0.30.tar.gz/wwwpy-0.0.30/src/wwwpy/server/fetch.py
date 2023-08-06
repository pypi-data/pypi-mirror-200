import urllib
import urllib.request

from wwwpy import HttpResponse


async def async_fetch_str(url: str, method: str = 'GET', data: str = '') -> str:
    response = sync_fetch_response(url, method=method, data=data)
    return response.content


def sync_fetch_response(url: str, method: str = 'GET', data: str = '') -> HttpResponse:
    def make_response(r):
        return HttpResponse(
            r.read().decode("utf-8"),
            r.headers.get_content_type()
        )

    if method != 'GET':
        if isinstance(data, str):
            data = bytes(data, 'utf8')
        rq = urllib.request.Request(url, method=method, data=data)
        with urllib.request.urlopen(rq) as r:
            return make_response(r)
    else:
        with urllib.request.urlopen(url) as r:
            return make_response(r)
