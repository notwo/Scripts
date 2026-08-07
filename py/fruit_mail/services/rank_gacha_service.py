from pages.rank_gacha_page import RankGachaPage
from services.base_game_service import BaseGameService


class RankGachaService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.gacha_page = RankGachaPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.rank_gacha_url

    async def play(self):
        while True:
            try:
                if await self.gacha_page.is_finished():
                    print("「ガチャの結果はこちら」を検出")
                    break
                #if await self.gacha_page.close_ad():
                #    continue
                # プレイ画面へ戻る
                await self.gacha_page.back_to_gacha()

                # ガチャを回す
                await self.gacha_page.click_button()

            except Exception as e:
                print(f"エラー: {e}")

        print("本日分のガチャ終了")