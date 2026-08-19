from pages.base_page import BasePage


class ScratchPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    async def scratch_link_count(self):
        return await self.page.locator(".scratch_link").count()

    def scratch_link(self, index):
        return self.page.locator(".scratch_link").nth(index)

    async def scratch_image_count(self):
        return await self.page.locator(".scratch_image").count()

    def scratch_image(self, index):
        return self.page.locator(".scratch_image").nth(index)