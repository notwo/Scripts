import time

from pages.prize_everyday_page import PrizeEverydayPage
from services.base_game_service import BaseGameService


class PrizeEverydayService(BaseGameService):

    def __init__(self, page, setting, browser):
        super().__init__(page, setting)
        self.prize_page = PrizeEverydayPage(page, setting)
        self.browser = browser

    @property
    def url(self) -> str:
        return self.setting.site.prize_everyday_url

    async def play(self):
        print("======== 毎日懸賞開始 ========")

        timeout = 1 * 60 * 1
        start_time = time.time()

        while True:
            try:
                print(time.time())
                if time.time() - start_time >= timeout:
                    await self.browser.close()
                    exit()

                options = await self.prize_page.get_apply_numbers()

                numeric_options = [
                    option
                    for option in options
                    if option["value"].isdigit()
                ]

                if not numeric_options:
                    print("応募できる口数がありません")
                    break

                max_option = max(
                    numeric_options,
                    key=lambda x: int(x["value"])
                )

                print(f"応募口数: {max_option['value']}")

                await self.prize_page.select_apply_number(
                    max_option["value"]
                )

                await self.prize_page.click_apply_button()

                await self.prize_page.click_confirm_button()

                await self.prize_page.click_confirm_button()

                await self.prize_page.click_final_apply_button()

            except Exception as e:
                await self.prize_page.close_ad()

        print("======== 応募完了 ========")
