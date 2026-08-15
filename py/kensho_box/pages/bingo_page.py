from pages.base_page import BasePage

# プレイして応募する
class BingoPage(BasePage):

    def __init__(self, page):
        self.page = page

    async def entry(self):
        """
        「プレイして応募する」リンク
        """
        link = self.page.get_by_role(
            "link",
            name="プレイして応募する"
        )
        if await link.is_visible():
            await link.click(timeout=1000)

    async def has_start_button(self):
        return await self.page.locator("#bingo_start").is_visible()

    async def click_start(self):
        await self.page.locator("#bingo_start").click()

    async def before_select_count(self):
        return await self.page.locator(".is_color.close").count()

    async def click_first_before_select(self):
        await self.page.locator(".is_color.close").first.click(timeout=1000)