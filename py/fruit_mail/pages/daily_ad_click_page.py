from pages.base_page import BasePage


class DailyAdClickPage(BasePage):

    def __init__(self, page):
        self.page = page

    async def link_count(self) -> int:
        return await self.page.get_by_role(
            "link",
            name="クリックで1pt"
        ).count()

    def target_link(self, index):
        return self.page.get_by_role(
            "link",
            name="クリックで1pt"
        ).nth(index)
