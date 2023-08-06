from __future__ import annotations

from collections.abc import Generator
from collections.abc import Iterable
from typing import Generic
from typing import TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    __slots__ = ('value', 'prev', 'next')

    def __init__(
        self,
        value: T,
        prev: Node | None = None,
        next: Node | None = None,  # noqa: A002
    ) -> None:
        self.value = value
        self.prev = prev
        self.next = next

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={self.value!r})'


class LinkedList(Generic[T]):
    __slots__ = ('head', 'tail', 'n')

    def __init__(self, nodes: Iterable[Node[T]] | None = None) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self.n = 0
        for node in (nodes or []):
            self.append(node)

    def _decrement_n(self) -> None:
        self.n = max(self.n - 1, 0)

    def append(self, node: Node[T]) -> None:
        self.n += 1
        if self.head is None:
            self.head = self.tail = node
            return

        assert self.tail is not None
        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    def remove(self, node: Node[T]) -> None:
        self._decrement_n()
        if node == self.tail:
            self.pop()
            return

        if node == self.head:
            self.popleft()
            return

        assert node.prev is not None
        assert node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev

    def popleft(self) -> Node[T] | None:
        """Pops from the left side (the head)"""
        self._decrement_n()
        if self.head is None:
            return None

        out_node = self.head
        if self.head.next is None:
            self.head = self.tail = None
            return out_node

        self.head = self.head.next
        self.head.prev = None
        return out_node

    def pop(self) -> Node[T] | None:
        """Pops from the Linked List (the tail)"""
        self._decrement_n()
        if self.tail is None:
            return None

        out_node = self.tail
        if self.tail.prev is None:
            self.head = self.tail = None
            return out_node

        self.tail = self.tail.prev
        self.tail.next = None
        return out_node

    def __iter__(self) -> Generator[Node[T], None, None]:
        cur_node = self.head
        while cur_node:
            yield cur_node
            cur_node = cur_node.next

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({list(self)})'

    def __len__(self) -> int:
        return self.n
