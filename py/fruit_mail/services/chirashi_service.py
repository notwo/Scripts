from pages.chirashi_page import ChirashiPage
from services.base_game_service import BaseGameService


class ChirashiService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.chirashi_page = ChirashiPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.chirashi_url

    async def play(self):
        await self.chirashi_page.search_by_zipcode()

        await self.chirashi_page.click_button()

        print("チラシクリック終了")