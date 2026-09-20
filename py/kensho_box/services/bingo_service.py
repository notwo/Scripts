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
        print("======== ビンゴ開始 ========")

        if await self.bingo_page.cleared():
            # TODO: 後で申し込みの部分自動化
            print("ビンゴクリア")
            return

        if await self.bingo_page.finished():
            print("======== ビンゴ終了 ========")
            return

        while True:
            try:
                result = await self._run()
                if not result:
                    break

            except Exception as e:
                await self.bingo_page.close_ad()

        print("======== ビンゴ終了 ========")

    async def _run(self):
        await self.bingo_page.entry()

        await asyncio.sleep(3)

        await self.bingo_page.click_first_before_select()

        if await self.bingo_page.before_select_count() >= 4:
            return False

        return True
