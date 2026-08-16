import random
from itertools import combinations
from typing import Iterator

from db.proverb_repository import ProverbRepository


class ProverbSolver:
    """ことわざペアの候補探索（DB優先＋ブルートフォース フォールバック）"""

    def __init__(self):
        pass

    def find_proverb_combo(
        self,
        available: list[str], repo: ProverbRepository
    ) -> tuple[str, str] | None:
        """
        DBに問い合わせてことわざの正解ペアを探す。
        見つからなければ None を返す（＝ブルートフォースへフォールバックする合図）。
        """
        for first in available:
            rest = [k for k in available if k != first]

            for second in rest:
                if repo.exists(first, second):
                    return (first, second)

        return None

    def generate_candidates(
        self,
        available: list[str], shuffle: bool = False
    ) -> Iterator[tuple[str, str]]:
        """
        DBに存在しない場合のブルートフォース用に、2個選ぶ全組み合わせを生成する。
        shuffle=True で試行順をランダム化する。
        """
        candidates = list(combinations(available, 2))
        if shuffle:
            random.shuffle(candidates)
        yield from candidates
