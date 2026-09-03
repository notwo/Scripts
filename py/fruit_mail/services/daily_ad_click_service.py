from pages.daily_ad_click_page import DailyAdClickPage
from services.base_game_service import BaseGameService


class DailyAdClickService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.ad_page = DailyAdClickPage(page)

    @property
    def url(self) -> str:
        return self.setting.site.daily_ad_click_url

    async def play(self):
        print("======== 毎日ポイント開始 ========")

        while True:
            try:
                count = await self.ad_page.link_count()

                if count == 0:
                    break

                for i in range(count):
                    link = self.ad_page.target_link(i)

                    if not await link.is_visible():
                        continue

                    before = len(self.page.context.pages)

                    await link.click()

                    await self.page.wait_for_timeout(5000)

                    if len(self.page.context.pages) > before:
                        new_page = self.page.context.pages[-1]

                        try:
                            await new_page.wait_for_load_state("domcontentloaded", timeout=5000)
                        finally:
                            await new_page.close()

                    else:
                        try:
                            await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                        except:
                            pass

                        await self.page.go_back()

                        try:
                            await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                        except:
                            pass

            except Exception as e:
                await self.ad_page.close_ad()

    print("======== 毎日ポイント終了 ========")

