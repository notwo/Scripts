from pages.chirashi_page import ChirashiPage
from services.base_game_service import BaseGameService


class ChirashiService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.chirashi_page = ChirashiPage(page)
        self.clicked = False

    @property
    def url(self) -> str:
        return self.setting.site.chirashi_url

    async def play(self):
        print("======== チラシクリック開始 ========")

        while True:
            try:
                if self.clicked:
                    break

                if not await self.chirashi_page.search_by_zipcode():
                    continue

                self.clicked = await self.chirashi_page.click_button()

            except Exception as e:
                await self.chirashi_page.close_ad()

        print("======== チラシクリック終了 ========")
