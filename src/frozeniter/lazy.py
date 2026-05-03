from collections.abc import Callable
from dataclasses import dataclass
from functools import cache

@dataclass
class LazyI[T]:
    supplier: Callable[[], T]

    @cache
    def get(self) -> T:
        return self.supplier()
