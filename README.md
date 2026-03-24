# YouTube Trend Analyzer

A simple command-line tool that uses the YouTube Data API to search for videos and store results in a DuckDB database for analysis.

## Features

- Search YouTube videos by keyword
- Store video data locally using DuckDB
- Analyze:
  - Top videos by view count
  - Average views per search term
- Easy-to-use command-line interface

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/yt-trend-analyzer.git
cd yt-trend-analyzer

Install the package:

pip install -e .

## Usage

Run the tool:

yt-trend --api-key YOUR_API_KEY --terms gaming coding python

Arguments:
- --api-key : Your YouTube Data API key (required)
- --terms : Search terms to query (space-separated)

Example:

yt-trend --api-key ABC123 --terms "game dev" "machine learning"

## How It Works

1. The program sends search requests to the YouTube API  
2. It retrieves video metadata and statistics  
3. Data is stored in a local DuckDB database  
4. SQL queries are used to analyze:
   - Most popular videos
   - Average performance per search term  
