from typing import NamedTuple, Union


class Request(NamedTuple):
    method: str
    content: Union[str, bytes]
    content_type: str
