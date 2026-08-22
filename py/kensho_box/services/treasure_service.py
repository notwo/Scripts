from pages.treasure_page import TreasurePage
from services.base_game_service import BaseGameService


class TreasureService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.treasure_page = TreasurePage(page)

    @property
    def url(self) -> str:
        return self.setting.site.treasure_url

    async def play(self):
        print("======== ポイント懸賞開始 ========")

        while True:
            try:
                if await self.treasure_page.finished():
                    print("======== 応募済み ========")
                    break

                await self.treasure_page.click_apply_button()

                await self.treasure_page.click_confirm_button()

                await self.treasure_page.click_confirm_button()

                await self.treasure_page.click_second_apply_button()

                await self.treasure_page.click_final_apply_button()
            except Exception as e:
                self.treasure_page.close_ad()

        print("======== ポイント懸賞終了 ========")