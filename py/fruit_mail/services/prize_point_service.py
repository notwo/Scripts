from pages.prize_point_page import PrizePointPage
from services.base_game_service import BaseGameService


class PrizePointService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.prize_page = PrizePointPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.prize_point_url

    async def play(self):
        print("======== ポイント懸賞開始 ========")

        while True:
            try:
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

        print("======== ポイント懸賞終了 ========")
