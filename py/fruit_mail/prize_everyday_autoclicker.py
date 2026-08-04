import asyncio
from playwright.async_api import async_playwright

LOGIN_ID = "5782102"
PASSWORD = "Mtmtms114514"


async def login(page):
    # ログインページ表示
    await page.goto("https://www.fruitmail.net/login?go_html=https://www.fruitmail.net/prize/everyday/")

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
    # select要素を取得
    select = page.locator('select[name="selected_apply_number"]')

    # option要素を取得
    options = await select.locator("option").evaluate_all("""
    options => options.map(o => ({
        value: o.value,
        text: o.textContent.trim()
    }))
    """)

    # 数値として解釈できるものだけ抽出
    numeric_options = [
        opt for opt in options
        if opt["value"].isdigit()
    ]

    if not numeric_options:
        print('プルダウンまたは数値が存在しません')
        return

    # valueが最大のものを取得
    max_option = max(numeric_options, key=lambda x: int(x["value"]))

    # 選択
    await select.select_option(value=max_option["value"])

    # 応募するボタン
    await page.locator('button[type="submit"]').click()

    # 確認して次へボタン
    await page.locator('button[type="submit"]').click()

    # 確認して次へボタン
    await page.get_by_role("button", name="確認して次へ").click()

    # 応募するボタン
    await page.get_by_role("button", name="応募する").click()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        # 毎日懸賞ページ
        await page.goto("https://www.fruitmail.net/prize/everyday/")

        # ログイン
        await login(page)

        # 毎日懸賞ページへ戻る
        await page.goto("https://www.fruitmail.net/prize/everyday/")

        await page.wait_for_load_state("domcontentloaded")

        await click_buttons(page)


asyncio.run(main())
