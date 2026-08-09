import asyncio

from pages.prize_roulette_page import PrizeRoulettePage
from services.base_game_service import BaseGameService


class PrizeRouletteService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.page = page
        self.roulette_page = PrizeRoulettePage(page)

    @property
    def url(self) -> str:
        return self.setting.site.prize_roulette_url

    async def play(self):
        print("======== プレゼントルーレット開始 ========")

        if await self.roulette_page.is_applied():
            print("======== プレゼントルーレット終了 ========")
            return

        await self.page.locator('button[type="submit"]').click()

        while True:
            try:
                #
                # 終了判定
                #
                if await self.roulette_page.is_finished():
                    print("======== プレゼントルーレット終了 ========")
                    break

                #
                # 広告を閉じる
                #
                if await self.roulette_page.close_ad():
                    await asyncio.sleep(1)
                    continue

                #
                # START / STOP / RETRY
                #
                button = await self.roulette_page.get_visible_button()

                if button:
                    selector, name = button

                    print(f"{name} をクリック")

                    await self.roulette_page.click_button(selector)

            except Exception as e:
                print(f"PrizeRouletteService Error: {e}")

            await asyncio.sleep(5)

        self.roulette_page.click_apply_button()
        self.roulette_page.click_confirm_button()
        self.roulette_page.click_confirm_button()
        self.roulette_page.click_final_apply_button()

        print("======== プレゼントルーレット終了 ========")