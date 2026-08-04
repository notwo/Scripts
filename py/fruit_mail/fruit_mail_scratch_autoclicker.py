import asyncio
from playwright.async_api import async_playwright

LOGIN_ID = "5782102"
PASSWORD = "Mtmtms114514"


BUTTONS = {
    "#start": "START",
    "#stop": "STOP",
    "#retry": "もういちど回す",
}


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



async def click_scratch(page):
    # 最初に件数を取得
    count = await page.locator(".scratch_link").count()

    for i in range(count):
        # locatorを毎回取り直す
        link = page.locator(".scratch_link").nth(i)

        if not await link.is_visible():
            continue

        print(f"{i + 1}/{count}")

        # クリック前のタブ数
        before = len(page.context.pages)

        # クリック
        await link.click()

        # タブが開くか少し待つ
        await page.wait_for_timeout(500)

        after = len(page.context.pages)

        if after > before:
            # 新しいタブが開いた
            new_page = page.context.pages[-1]

            try:
                await new_page.wait_for_load_state("domcontentloaded", timeout=5000)
            except:
                pass

            await new_page.close()

        else:
            # 同じタブで遷移した
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=5000)
            except:
                pass

            await page.go_back()

            try:
                await page.wait_for_load_state("domcontentloaded", timeout=5000)
            except:
                pass

    # ------------------------
    # scratch_imageを全てクリック
    # ------------------------
    images = page.locator(".scratch_image")
    image_count = await images.count()

    for i in range(image_count):
        image = page.locator(".scratch_image").nth(i)

        if await image.is_visible():
            await image.click()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        # スクラッチページへアクセス
        await page.goto("https://www.fruitmail.net/scratch/")

        # ログイン
        await login(page)

        # スクラッチをクリック
        await click_scratch(page)


asyncio.run(main())
