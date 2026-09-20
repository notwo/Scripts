"""メダルクリック（未クリックのメダルを開いてタブを閉じる）サービス"""
from playwright.async_api import Page


class AdKiller:
    def __init__(self, page: Page):
        self.page = page

    async def kill_ad(self) -> None:
        # ① 広告iframe
        await self._delete_iframe_ad()

        # ② 通常ページの広告
        await self._delete_standard_ad()

        # ③ AdSenseの下部固定広告
        #await self._delete_imobile_ad()

        #await self._delete_flexible_sticky_outer_ad()

    async def _delete_iframe_ad(self):
        for frame in list(self.page.frames):
            try:
                close = frame.locator(".gmoam_close")

                if await close.count() == 0:
                    continue

                if not await close.is_visible():
                    continue

                button = frame.locator(".gmoam_close_button")

                if await button.count() == 0:
                    continue

                await button.click(timeout=1000, force=True)
                return

            except Exception as e:
                # 広告iframeが再生成されることがあるので無視
                print(f"広告iframe更新: {type(e).__name__}")
                continue

    async def _delete_standard_ad(self):
        try:
            close = self.page.locator("#dismiss-button")

            if await close.count() > 0 and await close.is_visible():
                await close.click(timeout=1000, force=True)
                return

        except Exception as e:
            print(f"通常広告を閉じられませんでした: {type(e).__name__}")

    async def _delete_flexible_sticky_outer_ad(self):
        button = self.page.locator("#flexible-sticky-wiped-button")

        try:
            await button.wait_for(state="visible", timeout=3000)
            await button.click()
        except:
            pass

    async def _delete_imobile_ad(self):
        try:
            await self._delete_google_ad()

            # ③ AdSense / i-mobile等のDOM広告を削除
            # AdSense下部固定広告
            adsense = self.page.locator(
                "ins.adsbygoogle[data-anchor-status='displayed']"
            )

            count = await adsense.count()

            if count > 0:
                await adsense.evaluate_all(
                    "elements => elements.forEach(element => element.remove())"
                )
                print(f"AdSense固定広告を削除: {count}件")
                return

            # i-mobile全画面広告
            imobile = self.page.locator(
                "div[id^='im-'][data-imobile-creative-width]"
            )

            count = await imobile.count()

            if count > 0:
                await imobile.evaluate_all(
                    "elements => elements.forEach(element => element.remove())"
                )
                print(f"i-mobile広告を削除: {count}件")
                return

        except Exception as e:
            print(f"AdSense固定広告を削除できませんでした: {type(e).__name__}")

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
