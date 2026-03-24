from yt_trend_analyzer.analyzer import YouTubeTrendAnalyzer

def test_setup_db(tmp_path):
    """Test that the database and videos table are created."""

    db_path = tmp_path / "test.db"

    analyzer = YouTubeTrendAnalyzer("fake_key", str(db_path))
    analyzer.setup_db()

    result = analyzer.con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='videos';"
    ).fetchone()

    assert result is not None


def test_analyzer_initialization(tmp_path):
    """Test that the analyzer initializes correctly."""

    db_path = tmp_path / "test.db"
    analyzer = YouTubeTrendAnalyzer("fake_key", str(db_path))

    assert analyzer.con is not None
