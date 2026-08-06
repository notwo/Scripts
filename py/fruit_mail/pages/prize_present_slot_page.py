class PrizePresentSlotPage:

    BUTTONS = {
        "#start": "START",
        "#stop": "STOP",
        "#retry": "もういちど回す",
    }
    CLOSE_BUTTON_SELECTORS = [
        ".btn-close",
        ".smarttag-adx-inst__close-btn",
        "#btn-close-ad-interstitial",
    ]

    def __init__(self, page):
        self.page = page

    async def is_finished(self) -> bool:
        return await self.page.locator("#end").is_visible()

    async def close_ad(self) -> bool:
        """
        広告の閉じるボタンを探してクリックする

        Returns:
            True: 広告を閉じた
            False: 広告なし
        """

        for selector in self.CLOSE_BUTTON_SELECTORS:
            locator = self.page.locator(selector)

            count = await locator.count()

            for i in range(count):
                button = locator.nth(i)

                try:
                    if await button.is_visible():
                        await button.click()
                        print(f"{selector} をクリック")
                        return True
                except Exception:
                    # DOMが変わった場合などは次へ
                    continue

        return False

    async def visible_button(self):
        """
        表示されているボタンを返す
        Returns:
            tuple[str, str] | None
            (selector, name)
        """
        for selector, name in self.BUTTONS.items():
            locator = self.page.locator(selector)

            if await locator.is_visible():
                return selector, name

        return None

    async def click_button(self, selector: str):
        await self.page.locator(selector).click()