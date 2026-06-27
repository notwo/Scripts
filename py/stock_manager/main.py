from services.stock_service import StockService

CONFIG_FILE_PATH = "config"


def main():
    service = StockService(CONFIG_FILE_PATH)
    service.execute()


if __name__ == "__main__":
    main()
