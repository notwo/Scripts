"""メダルクリック（未クリックのメダルを開いてタブを閉じる）サービス"""
from playwright.async_api import Page


class MedalService:
    """
    (1) medal_icon_off.png を含む未クリックのメダル画像を取得
    (2) クリック
    (3) 開いた別タブを閉じる
    (4) 未クリックのメダルがなくなるまで繰り返す
    """

    def __init__(self, page: Page, setting):
        self._page = page
        self._off_marker = setting.campus.medal["medal_off_marker"]

    async def run(self) -> None:
        while True:
            target = await self._find_next_off_medal()
            if target is None:
                print("開くメダルがなくなりました。メダルクリック終了。")
                break

            async with self._page.context.expect_page() as popup_info:
                await target.click()
            popup = await popup_info.value
            await popup.close()
            print("メダルをクリックし、開いたタブを閉じました。")

    async def _find_next_off_medal(self):
        """medal_icon_off.png を含む最初の要素を返す（なければ None）"""
        items = self._page.locator(".click_medal_item")
        count = await items.count()

        for i in range(count):
            item = items.nth(i)
            src = await item.locator("img").get_attribute("src") or ""
            if self._off_marker in src:
                return item

        return None