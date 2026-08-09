import os
from pages.base_page import BasePage


class ChirashiPage(BasePage):

    def __init__(self, page):
        self.page = page

    async def search_by_zipcode(self):
        """
        郵便番号入力
        """
        zipcode_input = self.page.locator("#chirashi_zipcodeInput")
        if not await zipcode_input.is_visible():
            return

        zipcode = os.getenv("ZIPCODE")
        if not zipcode or not zipcode:
            print("郵便番号をハイフンなしで設定してください: ZIPCODE")
            return
        await zipcode_input.fill(zipcode)

        await self.page.locator("#chirashi_zipcodeButton").click()

    async def click_button(self):
        """
        チラシをクリック
        """
        chirashi = self.page.locator("a.chirashiComponent_chirashiList__link").first
        async with self.page.expect_popup() as popup_info:
            await chirashi.click()
            # 新しく開いたタブを取得
            popup = await popup_info.value

            # 新しいタブを閉じる
            await popup.close()