import os
from pages.base_page import BasePage


class ChirashiPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    async def search_by_zipcode(self) -> bool:
        """
        郵便番号入力
        """
        zipcode_input = self.page.locator("#chirashi_zipcodeInput")
        if not await zipcode_input.is_visible():
            return False

        zipcode = os.getenv("ZIPCODE")
        if not zipcode or not zipcode:
            print("郵便番号をハイフンなしで設定してください: ZIPCODE")
            return False
        await zipcode_input.fill(zipcode)

        zipcode_button = self.page.locator("#chirashi_zipcodeButton")
        if await zipcode_button.is_visible():
            await zipcode_button.click()

        return True

    async def click_button(self) -> bool:
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

        return True
