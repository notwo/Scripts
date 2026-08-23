import asyncio

from pages.hidden_point_page import HiddenPointPage
from services.base_game_service import BaseGameService


class HiddenPointService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.hidden_point_page = HiddenPointPage(page)

    @property
    def url(self):
        return self.setting.site.hidden_point_url

    async def play(self):
        await self.click_links()

    async def click_links(self):
        print("======== 隠しポイント開始 ========")

        count = await self.hidden_point_page.hidden_point_link_count()

        for i in range(count):
            await asyncio.sleep(2)

            link = self.hidden_point_page.hidden_point_link(i)

            if not await link.is_visible():
                continue

            before = len(self.page.context.pages)

            await link.click()

            await self.page.wait_for_timeout(1000)

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

        print("======== 隠しポイント終了 ========")
