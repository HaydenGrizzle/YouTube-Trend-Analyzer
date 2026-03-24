# src/yt_trend_analyzer/main.py

import argparse
from yt_trend_analyzer.analyzer import YouTubeTrendAnalyzer

def main():
    """Command-line interface for YouTube Trend Analyzer."""

    parser = argparse.ArgumentParser(
        description="Analyze YouTube trends and store results in DuckDB."
    )

    parser.add_argument(
        "--api-key",
        required=True,
        help="Your YouTube Data API key"
    )

    parser.add_argument(
        "--terms",
        nargs="+",
        required=True,
        help="Search terms (space-separated)"
    )

    parser.add_argument(
        "--db",
        default="data/LocalDatabase_Yt.db",
        help="Path to the DuckDB database"
    )

    args = parser.parse_args()

    # Create analyzer object
    analyzer = YouTubeTrendAnalyzer(args.api_key, args.db)

    # Setup DB
    analyzer.setup_db()

    # Run search
    analyzer.search_and_store(args.terms)

    # Print results
    print("\nTop Videos:")
    for row in analyzer.get_top_videos():
        print(row)

    print("\nAverage Views per Term:")
    for row in analyzer.get_avg_views():
        print(row)

if __name__ == "__main__":
    main()
