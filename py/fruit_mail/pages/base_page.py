class BasePage:

    AD_CLOSE_SELECTORS = [
        ".btn-close",
        ".smarttag-adx-inst__close-btn",
        "#btn-close-ad-interstitial",
    ]

    def __init__(self, page):
        self.page = page

    async def close_ad(self) -> bool:
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
                    continue

        return False