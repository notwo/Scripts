import random
from itertools import combinations
from typing import Iterator

from db.complex_kanji_repository import ComplexKanjiRepository


class ComplexKanjiSolver:
    """難読漢字ペアの候補探索（DB優先＋ブルートフォース フォールバック）"""

    def __init__(self):
        pass

    def _is_kanji(self, s: str) -> bool:
        return any('\u4e00' <= c <= '\u9fff' for c in s)


    def _is_hiragana(self, s: str) -> bool:
        return any('\u3040' <= c <= '\u309f' for c in s)

    def find_kanji_combo(
        self,
        available: list[str], repo: ComplexKanjiRepository
    ) -> tuple[str, str] | None:
        """
        DBに問い合わせて難読漢字の正解ペアを探す。
        見つからなければ None を返す（＝ブルートフォースへフォールバックする合図）。

        難読漢字は順不同のため、
        repo.find() を使い、available内でどちらを先に見つけても、
        DBに保存されている内容にヒットすればその組み合わせを返す。
        """
        for first in available:
            rest = [k for k in available if k != first]

            for second in rest:
                pair = repo.find(first, second)
                if pair is not None:
                    return pair

        return None

    def generate_candidates(
        self,
        available: list[str], shuffle: bool = False
    ) -> Iterator[tuple[str, str]]:
        """
        DBに存在しない場合のブルートフォース用に、2個選ぶ全組み合わせを生成する。
        shuffle=True で試行順をランダム化する。
        """
        candidates = [
            pair
            for pair in combinations(available, 2)
            if (
                (self._is_kanji(pair[0]) and self._is_hiragana(pair[1]))
                or
                (self._is_hiragana(pair[0]) and self._is_kanji(pair[1]))
            )
        ]

        if shuffle:
            random.shuffle(candidates)

        yield from candidates