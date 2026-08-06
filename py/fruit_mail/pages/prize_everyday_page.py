class PrizeEverydayPage:

    def __init__(self, page):
        self.page = page

    async def get_apply_numbers(self) -> list[dict]:
        """
        応募口数のプルダウンを取得する
        """

        select = self.page.locator(
            'select[name="selected_apply_number"]'
        )

        return await select.locator("option").evaluate_all(
            """
            options => options.map(o => ({
                value: o.value,
                text: o.textContent.trim()
            }))
            """
        )

    async def select_apply_number(self, value: str):

        await self.page.locator(
            'select[name="selected_apply_number"]'
        ).select_option(value=value)

    async def click_apply_button(self):
        """
        最初の「応募する」
        """
        await self.page.get_by_role(
            "button",
            name="応募する"
        ).click()

    async def click_confirm_button(self):
        """
        「確認して次へ」
        """
        await self.page.get_by_role(
            "button",
            name="確認して次へ"
        ).click()

    async def click_final_apply_button(self):
        """
        最後の「応募する」
        """
        await self.page.get_by_role(
            "button",
            name="応募する"
        ).click()