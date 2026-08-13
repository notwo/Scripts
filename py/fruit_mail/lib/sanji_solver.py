import random
from itertools import permutations
from typing import Iterator

from db.idiom_repository import IdiomRepository


class SanjiSolver:
    """三字熟語の候補探索（DB優先＋ブルートフォース フォールバック）"""

    def __init__(self):
        pass

    def find_sanji_combo(
        self,
        available: list[str], repo: IdiomRepository
    ) -> tuple[str, str, str] | None:
        """
        DBに問い合わせて三字熟語の組み合わせを探す（前方一致による枝刈りあり）。
        見つからなければ None を返す（＝ブルートフォースへフォールバックする合図）。
        """
        for first in available:
            rest1 = [k for k in available if k != first]

            for second in rest1:
                prefix = first + second
                if not repo.has_prefix(prefix):
                    continue

                rest2 = [k for k in rest1 if k != second]
                for third in rest2:
                    word = prefix + third
                    if repo.exists(word):
                        return (first, second, third)

        return None


    def generate_candidates(
        self,
        available: list[str], shuffle: bool = False
    ) -> Iterator[tuple[str, str, str]]:
        """
        DBに存在しない場合のブルートフォース用に、3個選ぶ全順列を生成する。
        shuffle=True で試行順をランダム化する。
        """
        candidates = list(permutations(available, 3))
        if shuffle:
            random.shuffle(candidates)
        yield from candidates