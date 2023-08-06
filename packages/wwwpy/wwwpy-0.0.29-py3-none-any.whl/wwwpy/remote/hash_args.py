from __future__ import annotations


def hash_args(content: str | None = None) -> dict:
    result = dict()
    if content is None:
        from js import window
        content = window.location.hash.removeprefix('#')
    for entry in content.split('&'):
        parts = entry.split('=', 1)
        key = parts[0]
        value = parts[1] if len(parts) > 1 else ''
        result[key] = value
    return result


def test_hash_args():
    target = hash_args('widget=W1')
    assert target == {'widget': 'W1'}


def test_hash_args_withNoValue():
    assert hash_args('noval') == {'noval': ''}
    assert hash_args('noval=') == {'noval': ''}


def test_hash_args_multiple():
    assert hash_args('a=1&b=2') == {'a': '1', 'b': '2'}
