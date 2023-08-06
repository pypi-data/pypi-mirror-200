from pathlib import Path

from wwwpy.resources import stacktrace_pathfinder, _path_is_contained


def test_external_filename():
    actual = stacktrace_pathfinder()
    assert actual == Path(__file__).resolve()


def test_is_contained_into():
    assert _path_is_contained(Path('/foo/bar'), Path('/foo/bar/baz')) is False


def test_is_contained_into_2():
    assert _path_is_contained(Path('/foo/xxx'), Path('/foo/bar/baz')) is False


def test_is_contained_into_3():
    assert _path_is_contained(Path('/foo/bar/baz/yyy'), Path('/foo/bar/baz')) is True


def test_is_contained_into_4():
    assert _path_is_contained(Path('/foo/bar/baz'), Path('/foo/bar/baz')) is True
