from ipo_screenshot import ScreenShotCollctor


def main():
    pipo = ScreenShotCollctor("config/setting.yml")
    pipo.launch()


if __name__ == "__main__":
    main()
