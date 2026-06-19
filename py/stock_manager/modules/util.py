from pathlib import Path
import yaml


class Util:
    @staticmethod
    def load_config(filename: str):
        config_file = Path(filename)

        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        return config
