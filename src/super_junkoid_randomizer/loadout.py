from collections import Counter
from typing import TYPE_CHECKING, Any, Iterable, Iterator, Optional, Union

from .item import Item
from .logic_shortcut import LogicShortcut

if TYPE_CHECKING:
    from game import Game


class ItemCounter(Counter[Item]):
    def __contains__(self, x: Any) -> bool:
        return self[x] > 0


class Loadout:
    contents: ItemCounter

    def __init__(self, game: "Game", items: Optional[Iterable[Item]] = None) -> None:
        self.game = game
        self.contents = ItemCounter(items)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Loadout):
            return False
        return (
                (self.contents == __o.contents) and
                (self.game is __o.game)
        )

    def __contains__(self, x: Union[Item, LogicShortcut]) -> bool:
        if isinstance(x, LogicShortcut):
            return x.access(self)
        return self.contents[x] > 0

    def __iter__(self) -> Iterator[Item]:
        for item, count in self.contents.items():
            for _ in range(count):
                yield item

    def __len__(self) -> int:
        return sum(self.contents.values())  # `Counter.total()` requires python 3.10

    def __repr__(self) -> str:
        return f"Loadout({self.game}, {self.contents})"

    def count(self, item: Item) -> int:
        return self.contents[item]

    def append(self, item: Item) -> None:
        self.contents[item] += 1

    def has_all(self, *items: Union[Item, LogicShortcut]) -> bool:
        return all(x in self for x in items)

    def has_any(self, *items: Union[Item, LogicShortcut]) -> bool:
        return any(x in self for x in items)

    def copy(self) -> "Loadout":
        return Loadout(self.game, self.contents)
