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
        await self.page.reload(wait_until="domcontentloaded")

        while True:
            try:
                if await self.slot_page.is_finished():
                    print("プレゼントトップへボタンを検出")
                    return

                if await self.slot_page.close_ad():
                    await asyncio.sleep(1)
                    continue
                else:
                    print('だめだったでち')

                button = await self.slot_page.visible_button()
                print('ittinpo')

                if button:
                    selector, name = button

                    print(f"{name} をクリック")

                    await self.slot_page.click_button(selector)

            except Exception as e:
                print(f"エラー: {e}")

            await asyncio.sleep(5)