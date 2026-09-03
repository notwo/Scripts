import asyncio

from lib.calculate_solver import CalculateSolver
from pages.campus.calculate_page import CalculatePage
from services.campus.medal_service import MedalService


class CalculateService():
    def __init__(self, page, setting):
        self.page = page
        self.calculate_page = CalculatePage(page)
        self.solver = CalculateSolver()
        self.medal_service = MedalService(page=page,setting=setting)
        self.setting = setting

    async def game_start(self):
        print("======== 四則演算記号ゲーム開始 ========")

        while True:
            try:
                if await self.calculate_page.is_finished():
                    await self.medal_service.run()
                    break

                await self._run()

                await self.calculate_page.transfer_check()

            except Exception as e:
                print(f"Calculate Game Error: {e}")
                # タイムアウトするときは大概広告のせい
                await self.calculate_page.close_ad()

            await asyncio.sleep(5)

        print("======== 四則演算記号ゲーム終了 ========")

    async def _run(self):
        await asyncio.sleep(2)

        items = self.page.locator(".shisokuenzanSelect")
        if await items.count() == 0:
            return

        numbers = await self.page.locator(".shisokuenzanUserAnswer__number").all()
        last_numbers = self.page.locator(".shisokuenzanUserAnswer__solve")
        if not await last_numbers.first.is_visible():
            return

        last_number_text = await last_numbers.first.inner_text()

        number_values = []

        for number in numbers:
            value = await number.inner_text()
            number_values.append(int(value))
        number_values.append(int(last_number_text))

        correct_signs = self.solver.find_operators(*number_values)

        for correct_sign in correct_signs:
            for i in range(await items.count()):
                item = items.nth(i)
                text = await item.inner_text()

                if text == correct_sign:
                    await item.click(timeout=1000)
                    break

        await self.calculate_page.click_check()
        await self.calculate_page.click_next()
