from services.stock_service import StockService


def test_specify_attachment_files(tmp_path, monkeypatch):
    dist = tmp_path / "dist"
    dist.mkdir()

    (dist / "stocks.csv").touch()
    (dist / "us_AI.pdf").touch()
    (dist / "ja_ゲーム.pdf").touch()

    monkeypatch.chdir(tmp_path)

    service = StockService.__new__(StockService)

    result = sorted(service._specify_attachment_files())

    assert result == [
        "dist/ja_ゲーム.pdf",
        "dist/stocks.csv",
        "dist/us_AI.pdf",
    ]
