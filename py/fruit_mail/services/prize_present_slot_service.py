import asyncio

from pages.prize_present_slot_page import PrizePresentSlotPage
from services.base_game_service import BaseGameService


class PrizePresentSlotService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.page = page
        self.slot_page = PrizePresentSlotPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.prize_present_slot_url

    async def play(self):
        print("======== プレゼントスロット開始 ========")

        await self.page.reload(wait_until="domcontentloaded")

        while True:
            try:
                if await self.slot_page.is_finished():
                    print("======== プレゼントトップへボタンを検出 ========")
                    countdown = self.page.locator("span.countdown")

                    h = await countdown.locator("#h").inner_text()
                    m = await countdown.locator("#m").inner_text()
                    s = await countdown.locator("#s").inner_text()

                    print(f"次回開始まで残り {h}:{m}:{s}")
                    break

                if await self.slot_page.close_ad():
                    await asyncio.sleep(1)
                    continue

                button = await self.slot_page.visible_button()

                if button:
                    selector, name = button

                    print(f"{name} をクリック")

                    await self.slot_page.click_button(selector)

            except Exception as e:
                await self.slot_page.close_ad()

            await asyncio.sleep(5)

        print("======== プレゼントスロット終了 ========")