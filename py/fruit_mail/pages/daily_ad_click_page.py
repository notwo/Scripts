from pages.base_page import BasePage


class DailyAdClickPage(BasePage):

    def __init__(self, page, setting):
        super().__init__(page, setting=setting)

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
