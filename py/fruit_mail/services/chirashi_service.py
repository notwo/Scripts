import time

from pages.chirashi_page import ChirashiPage
from services.base_game_service import BaseGameService


class ChirashiService(BaseGameService):

    def __init__(self, page, setting, browser):
        super().__init__(page, setting)
        self.chirashi_page = ChirashiPage(page, setting)
        self.clicked = False
        self.browser = browser

    @property
    def url(self) -> str:
        return self.setting.site.chirashi_url

    async def play(self):
        print("======== チラシクリック開始 ========")

        timeout = 1 * 20
        start_time = time.time()
        while True:
            try:
                print(time.time() - start_time)
                print(timeout)
                if time.time() - start_time >= timeout:
                    await self.browser.close()
                    exit()

                if self.clicked:
                    break

                if not await self.chirashi_page.search_by_zipcode():
                    continue

                self.clicked = await self.chirashi_page.click_button()

            except Exception as e:
                await self.chirashi_page.close_ad()

        print("======== チラシクリック終了 ========")
