from __future__ import annotations

import inspect
import zipfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Callable, Iterator, Iterable

from .http_request import Request
from .http_response import HttpResponse


@dataclass(frozen=True)
class Resource(ABC):
    arcname: str

    @abstractmethod
    def get_content(self) -> str:
        pass


@dataclass(frozen=True)
class StringResource(Resource):
    content: str

    def get_content(self) -> str:
        return self.content


@dataclass(frozen=True)
class PathResource(Resource):
    filepath: Path

    def get_content(self) -> str:
        return self.filepath.read_text()


class Bundles:
    def __init__(self):
        self.list: List[Bundle] = []
        self.strategy = strategy_no_cache

    def to_response(self, request: Request) -> HttpResponse:
        return HttpResponse.application_zip(self.strategy(self.list))

    def add_resources(self, resource_generator: CallableResourceIterator):
        self.list.append(LambdaBundle(resource_generator))

    def add_flat_folder(self, folder: Path, relative_to: Optional[Path] = None):
        self.add_resources(lambda: from_filesystem_once(folder, relative_to=relative_to))

    def add_file_content(self, filename: str, content: str):
        resource_list = [StringResource(filename, content)]
        self.list.append(LambdaBundle(lambda: resource_list))


def stacktrace_pathfinder(stack_backtrack=1) -> Optional[Path]:
    wwwpy_root = Path(__file__).resolve().parent

    for stack in inspect.stack():
        source_path = Path(stack.filename).resolve()
        if not _path_is_contained(source_path, wwwpy_root):
            stack_backtrack -= 1
            if stack_backtrack == 0:
                return source_path

    return None


def _path_is_contained(child: Path, parent: Path):
    cl = len(child.parts)
    cp = len(parent.parts)
    if cl < cp:
        return False
    m = min(cl, cp)
    child_parts = child.parts[:m]
    parent_parts = parent.parts[:m]
    return child_parts == parent_parts


CallableResourceIterator = Callable[[], Iterator[Resource]]


class Bundle(ABC):

    @abstractmethod
    def list(self) -> Iterable[Resource]:
        pass


class WatchableBundle(Bundle, ABC):
    @abstractmethod
    def is_changed(self):
        pass


def flatten_bundles(bundle_list: List[Bundle]) -> Iterable[Resource]:
    for bundle in bundle_list:
        yield from bundle.list()


class LambdaBundle(Bundle):
    def __init__(self, resource_generator: CallableResourceIterator):
        self.resource_generator = resource_generator

    def list(self) -> Iterable[Resource]:
        return self.resource_generator()


def strategy_no_cache(bundles: List[Bundle]) -> bytes:
    return build_archive(flatten_bundles(bundles))


def default_resource_filter(resource: Resource) -> Optional[Resource]:
    if not isinstance(resource, PathResource):
        return resource
    resource: PathResource
    filepath = resource.filepath
    if filepath.name == '.DS_Store':
        return None
    if filepath.name == '__pycache__' and filepath.is_dir():
        return None
    return resource


ResourceIterator = Iterator[Resource]
ResourceFilter = Callable[[Resource], Optional[Resource]]


def from_filesystem_once(
        folder: Path, relative_to: Optional[Path] = None,
        resource_filter: ResourceIterator = default_resource_filter
) -> Iterator[PathResource]:
    if relative_to is None:
        relative_to = folder

    def recurse(path: Path):
        for f in path.glob('*'):
            rel = f.relative_to(relative_to)
            candidate = PathResource(str(rel), f)
            item = resource_filter(candidate)
            if item is not None:
                if f.is_file():
                    yield item
                else:
                    yield from recurse(f)

    yield from recurse(folder)
    return iter(())


def build_archive(item_iterator: Iterator[Resource]) -> bytes:
    stream = BytesIO()
    zf = zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1)

    for item in item_iterator:
        if isinstance(item, PathResource):
            zf.write(item.filepath, item.arcname)
        elif isinstance(item, StringResource):
            zf.writestr(item.arcname, item.get_content())
        else:
            raise Exception(f'Unhandled class \n  type={type(item).__name__} \n  data={item}')
    zf.close()

    stream.seek(0)
    return stream.getbuffer().tobytes()
