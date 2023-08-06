from __future__ import annotations

from collections import defaultdict
from collections.abc import Generator
from collections.abc import Iterable
from copy import deepcopy
from typing import Generic

import search_string.constants as const
from search_string.constants import Data
from search_string.linked_list import LinkedList
from search_string.linked_list import Node
from search_string.search_string import SearchString


class Trie(Generic[Data]):
    __slots__ = ('trie', 'end_tokens')

    def __init__(self) -> None:
        self.trie: dict[str, Trie] = {}
        self.end_tokens: set[tuple[Data, int]] | None = None

    def __getitem__(self, key: str) -> Trie:
        return self.trie[key]

    def __setitem__(self, key: str, value: Trie) -> None:
        self.trie[key] = value

    def __contains__(self, char: str) -> bool:
        return char in self.trie

    @property
    def has_children(self) -> bool:
        return len(self.trie) > 0


class SearchStringCollection(Generic[Data]):
    def __init__(self, search_strings: Iterable[SearchString[Data]]) -> None:
        self.search_strings = self._build_search_string_dict(search_strings)
        self.trie: Trie[Data] = self._build_trie()

    def _build_search_string_dict(
        self,
        search_strings: Iterable[SearchString[Data]],
    ) -> dict[Data, SearchString[Data]]:
        out_dict: dict[Data, SearchString[Data]] = {}
        for ss in search_strings:
            if ss.data is None:
                raise ValueError('SearchStringCollection does not support search strings with data=None')
            if ss.data in out_dict:
                raise ValueError(f'Search string data {ss.data} is not unique')
            out_dict[ss.data] = ss
        return out_dict

    def __iter__(self) -> Generator[SearchString[Data], None, None]:
        yield from self.search_strings.values()

    def __repr__(self) -> str:
        name = self.__class__.__name__
        n = len(self.search_strings)
        if n < 3:
            return f'{name}({list(self.search_strings.values())})'
        else:
            return f'{name}({n} search strings)'

    def __getitem__(self, key: Data) -> SearchString[Data]:
        return self.search_strings[key]

    def __len__(self) -> int:
        return len(self.search_strings)

    def _concat_matched_sentences(
        self,
        sentences: list[str],
        matched_sentence_indices: list[int],
    ) -> list[str]:
        """
        Returns a list of sentences that contain the matched search strings
        and a SENTENCE_BREAK between sentences that are not matched.
        It is expected that `matched_sentence_indices` is in sorted order.
        """
        matched_sentences = []
        last: int | None = None
        for sentence_index in matched_sentence_indices:
            if last is not None and sentence_index - last > 1:
                matched_sentences.append(const.SENTENCE_BREAK)

            sentence = sentences[sentence_index]
            matched_sentences.append(sentence[:const.MAX_SENTENCE_CHARS])
            last = sentence_index

        return matched_sentences

    def _split_part(self, part: str) -> list[str]:
        parts = (
            p.strip()
            for p in part.strip(' ;').removesuffix(const.GLOBAL).strip(' ;').split(';')
        )
        return [p for p in parts if p]

    def _add_part_to_trie(
        self,
        ss_id: Data,
        part_id: int,
        part_str: str,
        cur_trie: Trie[Data],
    ) -> None:
        if not part_str:
            if cur_trie.end_tokens is None:
                cur_trie.end_tokens = set()

            cur_trie.end_tokens.add((ss_id, part_id))
            return

        cur_char, next_chars = part_str[0], part_str[1:]
        next_trie = cur_trie.trie.setdefault(cur_char, Trie())
        self._add_part_to_trie(ss_id, part_id, next_chars, next_trie)

    def _build_trie(self) -> Trie[Data]:
        trie: Trie[Data] = Trie()
        for ss in self:
            for part_id, part_str in ss._raw_parts():
                for splitted_part in self._split_part(part_str):
                    self._add_part_to_trie(ss.data, part_id, splitted_part, trie)
        return trie

    def _text_yielder(self, text: str) -> Generator[str, None, None]:
        """
        Yield the text surrounded with chars that will be treated as word
        boundaries.
        """
        yield '\n'  # Possible beginning word break
        yield from text
        yield '\n'  # Possible ending word break
        yield '\n'  # Strings that matched the end and need one more char to get added

    def _match_single_text(self, text: str) -> set[tuple[Data, int]]:
        """
        Matches a single text against the search strings and returns a set of
        tuples of the form (search_string_id, part_id).
        """
        active_nodes: LinkedList[Trie] = LinkedList()
        matched: set[tuple[Data, int]] = set()
        for char in self._text_yielder(text):
            is_wb = char in const.WORD_BREAK_CHARS
            active_nodes.append(Node(self.trie))
            for node in list(active_nodes):
                if is_wb and const.WORD_BOUNDARY_CHAR in node.value:
                    new_trie = node.value[const.WORD_BOUNDARY_CHAR]
                    if new_trie.end_tokens is not None:
                        matched.update(new_trie.end_tokens)
                        if new_trie.has_children:
                            active_nodes.append(Node(new_trie))
                    else:
                        active_nodes.append(Node(new_trie))

                if char not in node.value:
                    active_nodes.remove(node)
                else:
                    new_trie = node.value[char]
                    node.value = new_trie
                    if new_trie.end_tokens is not None:
                        matched.update(new_trie.end_tokens)
                        if not new_trie.has_children:
                            active_nodes.remove(node)
        return matched

    def _match_sentence(self, sentence: str) -> list[SearchString[Data]]:
        """
        Match the search strings against the text and return a list of
        SearchString objects that matched the text.
        """
        matched = self._match_single_text(sentence.lower())
        ssid_bitstrings: defaultdict[Data, int] = defaultdict(int)
        for ss_id, part_id in matched:
            ssid_bitstrings[ss_id] += part_id

        matched_ss: list[SearchString[Data]] = []
        for ss_id, bitstring in ssid_bitstrings.items():
            ss = self.search_strings[ss_id]
            if bitstring == ss.match_bitstring:
                ss.matched_sentences = [sentence[:const.MAX_SENTENCE_CHARS]]
                matched_ss.append(ss)
        return matched_ss

    def _match_sentences(self, sentences: list[str]) -> list[SearchString[Data]]:
        """
        Match the search strings against the text and return a list of
        SearchString objects that matched the text.
        """
        sentences_lower = [s.lower() for s in sentences]
        all_text = '\n'.join(sentences_lower)
        global_matched_raw = self._match_single_text(all_text)
        global_matched = {
            (ss_id, part_id)
            for ss_id, part_id in global_matched_raw
            if self.search_strings[ss_id].is_global(part_id)
        }
        global_ssid_bitstrings: defaultdict[Data, int] = defaultdict(int)
        for ss_id, part_id in global_matched:
            global_ssid_bitstrings[ss_id] += part_id

        matched_ssids: defaultdict[Data, list[int]] = defaultdict(list)
        for i, sentence in enumerate(sentences_lower):
            local_ssid_bitstrings = deepcopy(global_ssid_bitstrings)
            for ss_id, part_id in self._match_single_text(sentence):
                local_ssid_bitstrings[ss_id] += part_id

            for ss_id, bitstring in local_ssid_bitstrings.items():
                ss = self.search_strings[ss_id]
                if bitstring == ss.match_bitstring:
                    matched_ssids[ss_id].append(i)

        matched_ss: list[SearchString[Data]] = []
        for ss_id, sentence_ids in matched_ssids.items():
            ss = self.search_strings[ss_id]
            ss.matched_sentences = self._concat_matched_sentences(sentences, sentence_ids)
            matched_ss.append(ss)

        return matched_ss

    def find_all(self, text: str | list[str]) -> list[SearchString[Data]]:
        """
        Finds all matches of the search strings for the text or list of text
        fragments. Returns a list of the matched searchstrings. If none is found,
        the list is empty. Should be used when there can be multiple matches.

        Example:
        >>> ss = [SearchString('test', str(i), '', data=i) for i in range(500)]
        >>> results = SearchString.find_all(['test 12', 'test 9'], ss)
        >>> [(r.data, r.matched_text) for r in results]
        [(1, 'test 12'), (2, 'test 12'), (9, 'test 9'), (12, 'test 12')]
        """
        return (
            self._match_sentences(text)
            if isinstance(text, list)
            else self._match_sentence(text)
        )

    def find_one(self, text: str | list[str]) -> SearchString[Data] | None:
        """
        Finds the first match of the search strings for the text or list of
        text fragments and returns the given search string. If no match is
        found, None is returned. Should be used when there logically only can
        be one match.

        Example:
        >>> ss = [SearchString('test', str(i), '', data=i) for i in range(500)]
        >>> result = SearchString.find_one('test 123', ss)
        >>> result.data if result else None
        1
        >>> result.matched_text if result else None
        'test 123'
        """
        res = self.find_all(text)
        return res[0] if res else None
