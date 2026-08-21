import asyncio

from lib.balance_solver import BalanceSolver, Judgement
from pages.campus.balance_page import BalancePage
from services.campus.medal_service import MedalService


class BalanceService():
    def __init__(self, page, setting):
        self.page = page
        self.balance_page = BalancePage(page)
        self.medal_service = MedalService(page=page,setting=setting)
        self.setting = setting

    async def game_start(self):
        print("======== バランスクイズ開始 ========")

        while True:
            try:
                if await self.balance_page.is_finished():
                    await self.medal_service.run()
                    break

                await self._run()

                await self.balance_page.click_check()
                await self.balance_page.click_next()

                await self.balance_page.transfer_check()

            except Exception as e:
                print(f"Balance Game Error: {e}")
                # タイムアウトするときは大概広告のせい
                await self.balance_page.close_ad()

            await asyncio.sleep(5)

        print("======== バランスクイズ終了 ========")

    async def _run(self):
        await asyncio.sleep(2)

        weights = self.page.locator(".balanceSelect")
        weight_desc = await weights.all_inner_texts()
        weight_desc = [int(w) for w in weight_desc]
        weight_desc.reverse()

        solver = BalanceSolver(weight_desc=weight_desc)

        while True:
            if solver.is_finished():
                break

            weight = solver.next_weight()

            await weights.filter(has_text=str(weight)).click()
            await asyncio.sleep(1)

            balance_status = self.page.locator("#balance_status")

            judgement = solver.judge(await balance_status.inner_text())
            if judgement is Judgement.CLEARED:
                break
            elif judgement is Judgement.UNDO:
                await weights.filter(has_text=str(weight)).click()
                await asyncio.sleep(1)

        solver.reset()
