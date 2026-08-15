from fractions import Fraction
from itertools import product

OPS = {
    '＋': lambda x, y: x + y,
    '−': lambda x, y: x - y,
    '×': lambda x, y: x * y,
    '÷': lambda x, y: (x / y) if y != 0 else None,
}


class CalculateSolver:
    def __init__(self):
        pass

    def find_operators(self, a, b, c, d):
        """
        a □ b □ c = d を満たす演算子(op1, op2)を1組返す。
        ×÷は+-より優先して計算する(通常の数式のルール)。
        解が複数ある場合はそのうちの1つを返し、解が無い場合はNoneを返す。
        """
        a, b, c, d = Fraction(a), Fraction(b), Fraction(c), Fraction(d)

        for op1, op2 in product(OPS.keys(), repeat=2):
            try:
                if op1 in ('×', '÷') and op2 in ('＋', '−'):
                    mid = OPS[op1](a, b)          # (a op1 b) op2 c
                    if mid is None:
                        continue
                    val = OPS[op2](mid, c)
                elif op1 in ('＋', '−') and op2 in ('×', '÷'):
                    mid = OPS[op2](b, c)          # a op1 (b op2 c)
                    if mid is None:
                        continue
                    val = OPS[op1](a, mid)
                else:
                    mid = OPS[op1](a, b)          # 同じ優先度同士は左から計算
                    if mid is None:
                        continue
                    val = OPS[op2](mid, c)
            except ZeroDivisionError:
                continue

            if val is not None and val == d:
                return (op1, op2)

        return None