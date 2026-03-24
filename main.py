from googleapiclient.discovery import build
import duckdb
import os

api_key = "************"
youtube = build("youtube", "v3", developerKey = api_key)

os.makedirs("data", exist_ok=True)
con = duckdb.connect("data/LocalDatabase_Yt.db")
con.execute("DROP TABLE IF EXISTS videos")

# Create table (one time)
con.execute("""
CREATE TABLE IF NOT EXISTS videos(
    title TEXT,
    channel TEXT,
    published_at TEXT,
    thumbnail TEXT,
    view_count INTEGER,
    search_term TEXT
)
""")

search_terms = [
    "game dev",
    "i made a game",
    "making a game",
    "i tried making a game"
]

for term in search_terms:
    print(f"Searching: {term}")

    # Search videos
    search_response = youtube.search().list(
        q = term,
        part = "snippet",
        maxResults = 5,
        type = "video"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    # Getting stats
    video_response = youtube.videos().list(
        part = "statistics",
        id = ",".join(video_ids)
    ).execute()

    # Store it
    for i, item in enumerate(search_response["items"]):
        snippet = item["snippet"]

        title = snippet["title"]
        channel = snippet["channelTitle"]
        published_at = snippet["publishedAt"]
        thumbnail = snippet["thumbnails"]["high"]["url"]

        view_count = int(video_response["items"][i]["statistics"]["viewCount"])

        con.execute("""
            INSERT INTO videos VALUES (?, ?, ?, ?, ?, ?)
        """, (title, channel, published_at, thumbnail, view_count, term))

# Analysis
print("\nTop 10 videos overall:")
results = con.execute("""
    SELECT title, view_count, search_term
    FROM videos
    ORDER BY view_count DESC
    LIMIT 10
""").fetchall()

for row in results:
    print(row)

print("\nAverage views per search term:")
avg = con.execute("""
    SELECT search_term, AVG(view_count) as avg_views
    FROM videos
    GROUP BY search_term
    ORDER BY avg_views DESC
""").fetchall()

for row in avg:
    print(row)
