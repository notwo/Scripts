from pages.campus.campus_page import CampusPage


class ArithmeticPage(CampusPage):
    def __init__(self, page):
        super().__init__(page)

    async def is_finished(self) -> bool:
        return await self.page.locator("#lead_tomorrow").is_visible()
