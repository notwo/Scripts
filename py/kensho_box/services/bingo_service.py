import asyncio
from datetime import datetime

from pages.bingo_page import BingoPage
from services.base_game_service import BaseGameService


class BingoService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.bingo_page = BingoPage(page)
        self._bingo_count = 0

    @property
    def url(self) -> str:
        return self.setting.site.bingo_url

    async def play(self):
        today = datetime.now()

        while True:
            try:
                print("======== ビンゴ開始 ========")

                result = await self._run(today=today)
                if not result:
                    print("======== ビンゴ終了 ========")
                    break

            except Exception as e:
                await self.ad_killer.kill_ad()

    async def _run(self, today: datetime):
        await self.bingo_page.entry()

        await asyncio.sleep(3)
        count = await self.bingo_page.before_select_count()

        click_count = min(
            self.setting.bingo.max_click,
            count,
        )

        # 土、日にしかクリックできない玉を考慮する
        if today.weekday() >= 5:
            if click_count == 2:
                return False
        else:
            if click_count == 1:
                return False

        # 土、日にしかクリックできない玉を避ける
        if today.weekday() >= 5 or (today.weekday() < 4 and self._bingo_count != 4):
            await self.bingo_page.click_first_before_select()

        self._bingo_count = self._bingo_count + 1

        return True
