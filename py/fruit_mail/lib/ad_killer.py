from urllib.parse import urlparse
from playwright.async_api import Page


class AdKiller:
    def __init__(self, page: Page, setting):
        self.page = page
        self.setting = setting

    def _invalid_domain(self) -> bool:
        current_url = self.page.url
        domain = urlparse(current_url).netloc
        return domain not in self.setting.site.allowed_domain

    async def kill_ad(self) -> None:
        # 別サイトに富んでたら戻る
        if self._invalid_domain():
            await self.page.go_back()

        # iframe対策
        for frame in list(self.page.frames):
            try:
                close = frame.locator("#close-banner-ad-interstitial")

                if await close.count() == 0:
                    continue

                if not await close.is_visible():
                    continue

                button = frame.locator("#btn-close-ad-interstitial")

                if await button.count() == 0:
                    continue

                await button.click(timeout=1000, force=True)
                return

            except Exception as e:
                # 広告iframeが再生成されることがあるので無視
                print(f"広告iframe更新: {type(e).__name__}")
                continue

        # 1種類とは限らないため、見つけるたびに要追加
        for frame in list(self.page.frames):
            try:
                close = frame.locator("#dismiss-button")

                if await close.count() == 0:
                    continue

                if not await close.is_visible():
                    continue

                button = frame.locator("#dismiss-button-element")

                if await button.count() == 0:
                    continue

                await button.click(timeout=1000, force=True)
                return

            except Exception as e:
                # 広告iframeが再生成されることがあるので無視
                print(f"広告iframe更新: {type(e).__name__}")
                continue

        # ② 通常ページの広告
        try:
            close = self.page.locator("#dismiss-button")

            if await close.count() > 0 and await close.is_visible():
                await close.click(timeout=1000, force=True)
                return True

            close = self.page.locator(".smarttag-adx-inst__close-btn")

            if await close.count() > 0 and await close.is_visible():
                await close.click(timeout=1000, force=True)
                return True

        except Exception as e:
            print(f"通常広告を閉じられませんでした: {type(e).__name__}")

        await self._delete_google_ad()

    async def _delete_google_ad(self):
        ad = self.page.locator(
            "ins.adsbygoogle.adsbygoogle-noablate"
            "[data-anchor-status='displayed']"
        )
        count = await ad.count()
        if count > 0:
            await ad.evaluate_all(
                "elements => elements.forEach(element => element.remove())"
            )
            print(f"AdSense固定広告を削除: {count}件")
