"""
天秤バランスゲームの解答アルゴリズムのみを実装したクラス。

呼び出し側が以下の手順を繰り返すことで、天秤を水平にできる。

  1. solver.next_weight() で「次に置くべき重り」を取得する
     (None が返れば、この問題については試すべき重りは尽きている)
  2. 呼び出し側でその重りを実際に置く(クリックする)
  3. 置いた後の状態文字列を solver.judge(state_text) に渡す
  4. 戻り値の Judgement に応じて呼び出し側が動く
       - CLEARED: 水平になった。終了してよい
       - KEEP   : 傾いてはいるが軽い方向。重りは置いたままにして次へ
       - UNDO   : 重すぎる。呼び出し側で今置いた重りを外すクリックをする

アルゴリズム:
  重り 1,3,9,27 は「超増加数列」(各値が、それより小さい値の合計より大きい:
  3>1, 9>1+3, 27>1+3+9)なので、大きい方から順に
  「置いてみて、重すぎたら外す」という貪欲法だけで必ず正解(水平)にたどり着ける。
"""

from enum import Enum
from typing import Optional


class Judgement(Enum):
    CLEARED = "cleared"  # 水平になった(正解)
    KEEP = "keep"        # 軽い方向に傾いている。置いたままにする
    UNDO = "undo"        # 重すぎる。呼び出し側で重りを外す必要がある


class BalanceSolver:
    """天秤バランスゲームを解くための純粋なアルゴリズム部分。"""

    # 大きい方から試すことで貪欲法が成立する(超増加数列)
    def __init__(self, weight_desc: list[int]):
        self._cursor = 0
        self.cleared = False
        self.weight_desc = weight_desc

    def reset(self) -> None:
        """次の問題に取り組む前に内部状態を初期化する。"""
        self._cursor = 0
        self.cleared = False

    def is_finished(self) -> bool:
        """試すべき重りがもう残っていないか。"""
        return self._cursor >= len(self.weight_desc)

    def next_weight(self) -> Optional[int]:
        """次に置くべき重りを返す。既にクリア済み、または試すべき重りが
        尽きている場合は None を返す。"""
        if self.cleared or self.is_finished():
            return None
        return self.weight_desc[self._cursor]

    @staticmethod
    def _is_cleared_text(state_text: str) -> bool:
        return "水平" in state_text

    @staticmethod
    def _is_over_text(state_text: str) -> bool:
        return "右" in state_text

    def judge(self, state_text: str) -> Judgement:
        """直近で next_weight() の重りを置いた後の状態文字列を渡し、
        その重りをどう扱うべきかを判定する。"""
        if self._is_cleared_text(state_text):
            self.cleared = True
            return Judgement.CLEARED

        self._cursor += 1

        if self._is_over_text(state_text):
            return Judgement.UNDO

        return Judgement.KEEP