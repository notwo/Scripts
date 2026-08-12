from pages.game_top_page import GameTopPage
from services.base_game_service import BaseGameService
from services.campus.sanji_service import SanjiService

from db.idiom_repository import IdiomRepository


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

    async def _sanji(self):
        with IdiomRepository(self.setting.campus.sanji['db']['filepath']) as repo:
          await self.top_page.click_sanji_link(gamename="三字熟語ゲーム")
          new_page = self.page.context.pages[-1]
          try:
              await new_page.wait_for_load_state("domcontentloaded", timeout=5000)
          finally:
              await new_page.locator("#start_game").click(timeout=5000)
              await self.top_page.click_game_start_dialog()
              # ここがゲーム本体
              sanji_service = SanjiService(self.page, repo, self.setting)
              await sanji_service.game_start()
              await new_page.close()

    async def play(self):
        print("======== ゲームトップ ========")

        # フルーツ学園に遷移
        await self.top_page.goto_campus(url=await self._campus_url())

        # ゲームごとに実行
        ## 三字熟語ゲーム
        if self.setting.campus.sanji['active']:
            await self._sanji()

        ## 他のゲーム

        print("======== ゲーム終了 ========")
