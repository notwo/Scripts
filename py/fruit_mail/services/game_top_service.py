from pages.game_top_page import GameTopPage
from services.base_game_service import BaseGameService
from services.campus.sanji_service import SanjiService
from services.campus.proverb_service import ProverbService
from services.campus.calculate_service import CalculateService
from services.campus.arithmetic_service import ArithmeticService

from db.idiom_repository import IdiomRepository
from db.proverb_repository import ProverbRepository


class GameTopService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.top_page = GameTopPage(page)
        self.setting = setting

    @property
    def url(self) -> str:
        return self.setting.site.game_top_url

    async def _campus_url(self):
        return self.setting.site.campus_url

    async def _calculate(self):
        await self.top_page.click_game_link(gamename="四則演算記号ゲーム")
        try:
            await self.ad_killer.kill_ad()
            await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
        finally:
            await self.page.locator("#start_game").click(timeout=5000)
            await self.top_page.click_game_start_dialog()
            # ここがゲーム本体
            calculate_service = CalculateService(self.page, self.setting)
            await calculate_service.game_start()

    async def _arithmetic(self):
        await self.top_page.click_game_link(gamename="計算ゲーム")
        try:
            await self.ad_killer.kill_ad()
            await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
        finally:
            await self.page.locator("#start_game").click(timeout=5000)
            await self.top_page.click_game_start_dialog()
            # ここがゲーム本体
            calculate_service = ArithmeticService(self.page, self.setting)
            await calculate_service.game_start()

    async def _sanji(self):
        with IdiomRepository(self.setting.campus.sanji['db']['filepath']) as repo:
            await self.top_page.click_game_link(gamename="三字熟語ゲーム")
            try:
                await self.ad_killer.kill_ad()
                await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
            finally:
                await self.page.locator("#start_game").click(timeout=5000)
                await self.top_page.click_game_start_dialog()
                # ここがゲーム本体
                sanji_service = SanjiService(self.page, repo, self.setting)
                await sanji_service.game_start()

    async def _proverb(self):
        with ProverbRepository(self.setting.campus.proverb['db']['filepath']) as repo:
            await self.top_page.click_game_link(gamename="ことわざクイズ")
            try:
                await self.ad_killer.kill_ad()
                await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
            finally:
                await self.page.locator("#start_game").click(timeout=5000)
                await self.top_page.click_game_start_dialog()
                # ここがゲーム本体
                proverb_service = ProverbService(self.page, repo, self.setting)
                await proverb_service.game_start()

    async def play(self):
        print("======== ゲームトップ ========")

        # フルーツ学園に遷移
        await self.top_page.goto_campus(url=await self._campus_url())

        # ゲームごとに実行
        ## 四則演算記号ゲーム
        if self.setting.campus.calculate['active']:
            await self._calculate()

        ## 計算ゲーム
        if self.setting.campus.arithmetic['active']:
            await self._arithmetic()

        ## 三字熟語ゲーム
        if self.setting.campus.sanji['active']:
            await self._sanji()

        ## ことわざクイズ
        if self.setting.campus.proverb['active']:
            await self._proverb()

        ## 他のゲーム

        print("======== ゲーム終了 ========")
