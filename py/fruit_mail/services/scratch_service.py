import asyncio
from pages.scratch_page import ScratchPage
from services.base_game_service import BaseGameService


class ScratchService(BaseGameService):

    def __init__(self, page, setting):
        super().__init__(page, setting)
        self.scratch_page = ScratchPage(page)

    @property
    def url(self):
        return self.setting.site.scratch_url

    async def play(self):
        print("======== スクラッチ開始 ========")

        await self.click_links()

        print("======== スクラッチ終了 ========")

    async def click_links(self):
        count = await self.scratch_page.scratch_link_count()

        for i in range(count):
            link = self.scratch_page.scratch_link(i)

            if not await link.is_visible():
                continue

            before = len(self.page.context.pages)

            await link.click()

            await self.page.wait_for_timeout(1000)

            if len(self.page.context.pages) > before:
                new_page = self.page.context.pages[-1]

                try:
                    await new_page.wait_for_load_state("domcontentloaded")
                finally:
                    await new_page.close()

                    await self.click_images(i)
            else:
                try:
                    await self.page.wait_for_load_state("domcontentloaded")
                except:
                    pass

                await self.click_images(i)

                await self.page.go_back()

                try:
                    await self.page.wait_for_load_state("domcontentloaded")
                except:
                    pass

    async def click_images(self, index: int):
        image = self.scratch_page.scratch_image(index)

        if await image.is_visible():
            await image.click()
