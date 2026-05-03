from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Self

from lazy import Lazy

@dataclass(frozen=True)
class frozeniter[T](Iterable[T]):
    value: T
    rest: Lazy[frozeniter[T] | None] | None

    def next(self) -> tuple[T, frozeniter[T] | None]:
        return self.value, self.rest.get() if self.rest is not None else None

    def get(self) -> T:
        return self.value

    def concat(self, other: Self) -> Self:
        rest = self.rest.get() if self.rest is not None else None
        match rest:
            case None:
                return type(self)(
                    self.value,
                    Lazy(lambda: None)
                )
            case _:
                return type(self)(
                    self.value,
                    Lazy(lambda: rest.concat(other))
                )

    def __iter__(self) -> Iterator[T]:
        yield self.value
        match self.rest.get() if self.rest is not None else None:
            case None:
                pass
            case next_frozeniter:
                yield from iter(next_frozeniter)

    @classmethod
    def of[U](cls, iterable: Iterable[U]) -> frozeniter[U] | None:
        iterator = iter(iterable)
        try:
            next_value = next(iterator)
            return frozeniter(next_value, Lazy(lambda: frozeniter.of(iterator)))
        except StopIteration:
            return None
