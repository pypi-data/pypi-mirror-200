"""Cart models."""
from collections import OrderedDict
from typing import List, Optional

from .fields import _StrField, _IntField


class CartItem:
    # pylint:disable=too-few-public-methods
    """Cart item."""

    name = _StrField(max_length=20)
    quantity = _IntField(min_value=1)
    amount = _IntField(min_value=0)
    description = _StrField(max_length=40)

    def __init__(
        self,
        name: str,
        quantity: int,
        amount: int,
        description: Optional[str] = None,
    ) -> None:
        self.name = name
        self.quantity = quantity
        self.amount = amount
        self.description = description

    def as_json(self) -> OrderedDict:
        """Return cart item as JSON."""
        item = OrderedDict(
            [
                ("name", self.name),
                ("quantity", self.quantity),
                ("amount", self.amount),
            ]
        )

        if self.description:
            item["description"] = self.description  # type: ignore
        return item


class Cart:
    # pylint:disable=too-few-public-methods
    """Cart."""

    def __init__(self, items: List[CartItem]) -> None:
        self._items = items

    def as_json(self) -> List[OrderedDict]:
        """Return cart as JSON array."""
        return [item.as_json() for item in self._items]
