from typing import Dict, List, Union

Header = Dict[str, str]
QueryParams = Dict[str, Union[str, List[str]]]

RawBody = Union[str, bytes]
Body = Dict[str, Union[str, bool, int]]
