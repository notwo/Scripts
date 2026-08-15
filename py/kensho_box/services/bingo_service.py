import asyncio
from pages.bingo_page import BingoPage
from services.base_game_service import BaseGameService


class BingoService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.bingo_page = BingoPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.bingo_url

    async def play(self):
        while True:
            try:
                print("======== ビンゴ開始 ========")

                result = await self._run()
                if result:
                    break

                print("======== ビンゴ終了 ========")

            except Exception as e:
                await self.ad_killer.kill_ad()

    async def _run(self):
        await self.bingo_page.entry()

        await asyncio.sleep(3)
        count = await self.bingo_page.before_select_count() + 1

        click_count = min(
            self.setting.bingo.max_click,
            count,
        )
        if click_count == 1:
            return False

        await self.bingo_page.click_first_before_select()

        return True
