from pages.prize_everyday_page import PrizeEverydayPage
from services.base_game_service import BaseGameService


class PrizeEverydayService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.prize_page = PrizeEverydayPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.prize_everyday_url

    async def play(self):
        print("======== 本日の日替わり懸賞開始 ========")

        while True:
            try:
                if await self.prize_page.finished():
                    print("======== 応募済み ========")
                    break

                await self.prize_page.click_apply_button()

                await self.prize_page.click_confirm_button()

                await self.prize_page.click_confirm_button()

                await self.prize_page.click_final_apply_button()

            except Exception as e:
                self.prize_page.close_ad()

        print("======== 応募完了 ========")
