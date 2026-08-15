import itertools


class ArithmeticSolver():
    def __init__(self):
        pass

    def solve_puzzle(self, template: str, target: int, digit_range=range(2, 10)):
        """
        template: '_' を□の代わりに使った数式文字列
                  例: "_ * _ + _"
        target  : 右辺の値
        戻り値  : (使った数字のタプル, 完成した式) or None(解なし)
        """
        n_blanks = template.count('_')

        for digits in itertools.product(digit_range, repeat=n_blanks):
            expr = template
            for d in digits:
                expr = expr.replace('_', str(d), 1)
            try:
                # 0除算などはスキップ
                if eval(expr) == target:
                    return digits, expr
            except ZeroDivisionError:
                continue

        return None  # 解なし
