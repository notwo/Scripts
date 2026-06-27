import logging
from pathlib import Path


class Logger:
    _logger = None

    @classmethod
    def get_logger(self, log_dir: str, logfile: str, loglevel: int = logging.INFO, reload: bool = False):
        if self._logger and not reload:
            return self._logger

        log_dir = Path(log_dir)
        log_dir.mkdir(exist_ok=True)

        logger = logging.getLogger("stock_manager")
        logger.setLevel(loglevel)

        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # コンソール出力
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # ファイル出力
        file_handler = logging.FileHandler(
            log_dir / logfile,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        self._logger = logger

        return logger
