"""
既知の難読漢字をあらかじめDBに登録するスクリプト。

使い方:
    python3 seed_kanji.py

SEED_PAIRS に登録したい漢字、ひらがなを追加してから実行してください。
config/setting.yml の campus.db.path で指定されたDBファイルに登録されます。
"""
from complex_kanji_repository import ComplexKanjiRepository
from pathlib import Path

import re


# ここに事前にわかっている難読漢字を追加してください(漢字（ひらがな）のフォーマット)
SEED_PAIRS = [
]


def kanji_pair(text: str) -> list[str]:
    match = re.match(r"^(.*?)（(.*?)）$", text)

    if match is None:
        raise ValueError(f"形式が不正です: {text}")

    return list(match.groups())

def main() -> None:
    db_path = Path("./db/campus.db").resolve()

    valid_kanjis = [kanji_pair(w) for w in SEED_PAIRS]

    with ComplexKanjiRepository(db_path) as repo:
        print(f"登録対象: {len(valid_kanjis)}件")

        repo.register_many(valid_kanjis)

        print(f"{len(valid_kanjis)}件を登録処理しました（DB: {db_path}）")


if __name__ == "__main__":
    main()