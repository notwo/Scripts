import time

from pages.rank_gacha_page import RankGachaPage
from services.base_game_service import BaseGameService


class RankGachaService(BaseGameService):

    def __init__(self, page, setting, browser):
        super().__init__(page, setting)
        self.gacha_page = RankGachaPage(page, setting)
        self.browser = browser

    @property
    def url(self) -> str:
        return self.setting.site.rank_gacha_url

    async def play(self):
        print("======== ガチャ開始 ========")

        timeout = 1 * 20
        start_time = time.time()
        while True: 
            try:
                print(time.time() - start_time)
                print(timeout)
                if time.time() - start_time >= timeout:
                    await self.browser.close()
                    exit()

                if await self.gacha_page.is_finished():
                    print("「ガチャの結果はこちら」を検出")
                    break
                await self.gacha_page.close_ad()

                # 動画の読み込みに失敗しました
                await self.gacha_page.ok_button()

                # プレイ画面へ戻る
                await self.gacha_page.back_to_gacha()

                # ガチャを回す
                await self.gacha_page.click_button()

            except Exception as e:
                print(f"エラー: {e}")
                await self.gacha_page.close_ad()

        print("======== ガチャ終了 ========")