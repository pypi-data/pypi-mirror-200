from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(init=False)
class Marker:
    args: List[Any]
    kwargs: Dict

    def __init__(self, *args, **kwargs):
        self.args = [*args]
        self.kwargs = {**kwargs}
