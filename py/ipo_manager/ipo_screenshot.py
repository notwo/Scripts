from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import yaml
from util import Util


class ScreenShotCollctor:
    def __init__(self, filename: str) -> None:
        self.config = None
        self.pages = self._load_pages(filename)

    def _load_pages(self, filename: str) -> list[dict]:
        config_file = Path(filename)

        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        return self.config["pages"]

    def launch(self, make_timestamp_folder: bool = True) -> None:
        output_dir = Path("screenshots")
        if make_timestamp_folder:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("screenshots") / timestamp

        print(f"[{Util.current_time()}]Save directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False
            )
            page = browser.new_page(
                viewport={"width": self.config['browser']['width'], "height": self.config['browser']['height']}
            )

            for page_info in self.pages:
                name = page_info["name"]
                url = page_info["url"]

                print(f"[{Util.current_time()}]Accessing: {url}")

                try:
                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=self.config['browser']['timeout']
                    )

                    page.screenshot(
                        path=output_dir / f"{name}.png",
                        full_page=True
                    )

                    print("  -> Success")

                except Exception as e:
                    print(f"  -> Failed: {e}")

            browser.close()
            print(f'[{Util.current_time()}]Done')
