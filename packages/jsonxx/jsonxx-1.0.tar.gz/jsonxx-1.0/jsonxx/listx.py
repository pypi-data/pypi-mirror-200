from .base import ExtensionBase
from typing import TypeVar, Self

T = TypeVar("T")

class ListX(ExtensionBase, list[T]):
    def __getitem__(self, key) -> T | None:
        if isinstance(key, slice) or key < len(self):
            return list.__getitem__(self, key)
        return None

    def __call__(self):
        return ListX()

    def map(self, transform, *transform_args, **transform_kwargs) -> Self:
        transformed = self()
        for element in self:
            transformed.append(
                transform(element, *transform_args, **transform_kwargs))
        return transformed

    def first(self) -> T:
        return self.get(0)

    def find(self, transform, *transform_args, **transform_kwargs) -> T:
        for item in self:
            if transform(item, *transform_args, **transform_kwargs):
                return item

    def find_all(self, transform, *transform_args, **transform_kwargs) -> Self:
        lst = self()
        for item in self:
            if transform(item, *transform_args, **transform_kwargs):
                lst.append(item)
        return lst

    def join(self, separator: str):
        return separator.join(self)

    def append(self, value) -> Self:
        super().append(value)
        self.save()
        return self

    def __add__(self, other) -> Self:
        if isinstance(other, list | ListX):
            self += other
            self.save()
        else:
            self.append(other)
        return self

    get = __getitem__
