"""
既知の三字熟語をあらかじめDBに登録するスクリプト。

使い方:
    python seed_idioms.py

SEED_WORDS に登録したい熟語（3文字）を追加してから実行してください。
config/setting.yml の campus.db.path で指定されたDBファイルに登録されます。
"""
from idiom_repository import IdiomRepository
from pathlib import Path


# ここに事前にわかっている三字熟語を追加してください（3文字であること）
SEED_WORDS = [
]

def main() -> None:
    db_path = Path("./db/campus.db").resolve()

    invalid = [w for w in SEED_WORDS if len(w) != 3]
    if invalid:
        print(f"⚠ 3文字でない単語が含まれています。登録をスキップします: {invalid}")

    valid_words = [w for w in SEED_WORDS if len(w) == 3]

    with IdiomRepository(db_path) as repo:
        print(f"登録対象: {len(valid_words)}件")

        # DBに既に存在する単語を確認
        existing = [w for w in valid_words if repo.exists(w)]

        if existing:
            print(f"⚠ 既にDBに存在するため登録されない単語: {existing}")
        else:
            print("✓ DB上の重複なし")

        repo.add_many(valid_words)
        print(f"{len(valid_words)}件を登録処理しました（DB: {db_path}）")


if __name__ == "__main__":
    main()