# src/yt_trend_analyzer/analyzer.py

from googleapiclient.discovery import build
from yt_trend_analyzer.constants import DEFAULT_MAX_RESULTS
import duckdb

class YouTubeTrendAnalyzer:
    """Analyze YouTube videos and store stats in DuckDB."""
    def __init__(self, api_key: str, db_path: str):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.con = duckdb.connect(db_path)

    def setup_db(self):
        """Create the videos table if it doesn't exist."""
        self.con.execute("""
        CREATE TABLE IF NOT EXISTS videos(
            title TEXT,
            channel TEXT,
            published_at TEXT,
            thumbnail TEXT,
            view_count INTEGER,
            search_term TEXT
        )
        """)

    def search_and_store(self, search_terms: list[str], max_results: int = DEFAULT_MAX_RESULTS):
        """Search YouTube for each term and store in the database."""
        for term in search_terms:
            print(f"Searching: {term}")

            search_response = self.youtube.search().list(
                q=term,
                part="snippet",
                maxResults=max_results,
                type="video"
            ).execute()

            video_ids = [item["id"]["videoId"] for item in search_response["items"]]

            video_response = self.youtube.videos().list(
                part="statistics",
                id=",".join(video_ids)
            ).execute()

            for i, item in enumerate(search_response["items"]):
                snippet = item["snippet"]
                view_count = int(video_response["items"][i]["statistics"]["viewCount"])

                self.con.execute("""
                    INSERT INTO videos VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    snippet["title"],
                    snippet["channelTitle"],
                    snippet["publishedAt"],
                    snippet["thumbnails"]["high"]["url"],
                    view_count,
                    term
                ))

    def get_top_videos(self, limit: int = 10):
        """Return top videos by view count."""
        return self.con.execute(f"""
            SELECT title, view_count, search_term
            FROM videos
            ORDER BY view_count DESC
            LIMIT {limit}
        """).fetchall()

    def get_avg_views(self):
        """Return average views per search term."""
        return self.con.execute("""
            SELECT search_term, AVG(view_count) as avg_views
            FROM videos
            GROUP BY search_term
            ORDER BY avg_views DESC
        """).fetchall()
