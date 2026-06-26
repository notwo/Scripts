from services.stock_service import StockService

CONFIG_FILE = "config/setting.yml"


def main():
    service = StockService(CONFIG_FILE)
    service.execute()


if __name__ == "__main__":
    main()
