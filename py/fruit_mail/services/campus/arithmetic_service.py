import asyncio

from lib.arithmetic_solver import ArithmeticSolver
from pages.campus.arithmetic_page import ArithmeticPage
from services.campus.medal_service import MedalService


class ArithmeticService():
    def __init__(self, page, setting):
        self.page = page
        self.arithmetic_page = ArithmeticPage(page)
        self.solver = ArithmeticSolver()
        self.medal_service = MedalService(page=page,setting=setting)
        self.setting = setting

    async def game_start(self):
        print("======== 計算ゲーム開始 ========")

        while True:
            try:
                if await self.arithmetic_page.is_finished():
                    await self.medal_service.run()
                    break

                await self._run()

                await self.arithmetic_page.transfer_check()

            except Exception as e:
                print(f"Arithmetic Game Error: {e}")
                # タイムアウトするときは大概広告のせい
                await self.arithmetic_page.close_ad()

            await asyncio.sleep(5)

        print("======== 計算ゲーム終了 ========")

    async def _run(self):
        await asyncio.sleep(2)

        items = self.page.locator("button.keisanSelect")
        signs = (await self.page.locator(".keisanUserAnswer__sign").all())[:-1]

        sign_texts = [await sign.inner_text() for sign in signs]
        template = f'_{"_".join(sign_texts)}_'
        template = (
            template
            .replace("×", "*")
            .replace("÷", "/")
            .replace("＋", "+")
            .replace("ー", "-")
        )

        keisan_solve = self.page.locator("#keisan_solve")
        if not await keisan_solve.is_visible():
            return
        keisan_solve_text = await keisan_solve.inner_text()

        correct_numbers, _ = self.solver.solve_puzzle(template=template, target=int(keisan_solve_text))

        for correct_number in correct_numbers:
            for i in range(await items.count()):
                item = items.nth(i)
                number = int(await item.inner_text())

                if number == correct_number:
                    await item.click(timeout=1000)
                    break

        await self.arithmetic_page.click_check()
        await self.arithmetic_page.click_next()
