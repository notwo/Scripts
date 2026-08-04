import asyncio
from playwright.async_api import async_playwright

LOGIN_ID = "5782102"
PASSWORD = "Mtmtms114514"


async def login(page):
    if await page.locator("#user_identifier").count() == 0:
        print("既にログイン済み")
        return

    # ID・パスワード入力
    await page.fill("#user_identifier", LOGIN_ID)
    await page.fill("#password", PASSWORD)

    # ログインボタン押下
    await page.locator('button[type="submit"]').click()

    # ② 広告が表示されていたら閉じる
    close_ad = page.locator("#btn-close-ad-interstitial")
    if await close_ad.is_visible():
        print("広告を閉じます")
        await close_ad.click()

        # 広告が閉じるのを少し待つ
        await asyncio.sleep(1)

    # ログイン後の画面が読み込まれるまで待機
    await page.wait_for_load_state("domcontentloaded")

    print("ログイン完了。リロードします。")

    # 一度リロード
    await page.reload()

    # ログイン完了を待機
    await page.wait_for_load_state("domcontentloaded")


async def click_buttons(page):
    if await page.locator('#bingo_start').is_visible():
        await page.locator('#bingo_start').click()

    buttons = page.locator("input.before_select")

    count = await buttons.count()

    print(f"{count}個のボタンがあります")

    click_count = min(4, count)

    for i in range(click_count):
        # 毎回取得し直す（クリックするとDOMが変わるため）
        button = page.locator("input.before_select").first
        await button.click()

        # before_select が1つ減るまで待つ
        await page.wait_for_function(
            "count => document.querySelectorAll('input.before_select').length < count",
            arg=count
        )
        count -= 1

    print("クリック完了")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        # ビンゴページ
        await page.goto("https://www.fruitmail.net/bingo/index.php")

        # ログイン
        await login(page)

        # ビンゴページへ戻る
        await page.goto("https://www.fruitmail.net/bingo/index.php")

        await page.wait_for_load_state("domcontentloaded")

        await click_buttons(page)


asyncio.run(main())
