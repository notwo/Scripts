class BasePage:

    AD_CLOSE_SELECTORS = [
        ".btn-close",
        ".smarttag-adx-inst__close-btn",
        "#btn-close-ad-interstitial",
    ]

    def __init__(self, page):
        self.page = page

    def wait_for_debug(self):
        self.page.wait_for_timeout(10000)

    async def close_ad(self) -> bool:
        """
        広告の閉じるボタンを探してクリックする

        Returns:
            True: 広告を閉じた
            False: 広告なし
        """
        for selector in self.AD_CLOSE_SELECTORS:
            locator = self.page.locator(selector)

            count = await locator.count()

            for i in range(count):
                target = locator.nth(i)

                try:
                    if await target.is_visible():
                        await target.click()
                        return True
                except Exception:
                    # DOMが変わった場合などは次へ
                    continue

        return False