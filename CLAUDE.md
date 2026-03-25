# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sports Scraper is a Python MVC application that aggregates sports news from YouTube (API v3) and BBC Sport (Selenium), stores data in MongoDB, runs VADER sentiment analysis, and provides a Tkinter desktop GUI for browsing results.

## Commands

```bash
# Run the GUI application
python gui/app.py

# Run tests (integration test that exercises scrapers → DB pipeline)
python test.py

# Launch EDA notebook
jupyter notebook notebooks/eda_sports.ipynb
```

## Prerequisites

- Python 3.8+ with a virtualenv
- MongoDB running locally (default: `mongodb://localhost:27017/`)
- Chrome browser installed (BBC scraper uses Selenium + headless Chrome)
- `.env` file at project root with: `YOUTUBE_API_KEY`, `MONGO_URI`, `MONGO_DB_NAME`

## Architecture

**MVC + Service Layer:**

- **models/post.py** — `Post` dataclass with `to_dict()` for MongoDB serialization. Fields: source, keyword, title, text, url, date, sentiment, likes.
- **scrapers/** — `BaseScraper` (ABC) defines `search()` and `get_source_name()`. `YouTubeScraper` uses Google API; `BBCScraper` uses Selenium + BeautifulSoup on the BBC Sport homepage.
- **db/mongo_handler.py** — MongoDB wrapper operating on the `posts` collection.
- **services/scraper_service.py** — Orchestrates scrapers, DB, and VADER sentiment analysis. Key entry point: `search_and_analyze(keyword, limit)`.
- **gui/app.py** — Tkinter GUI with threaded (daemon) search to avoid UI blocking. Stores application state as globals.
- **config.py** — Loads `.env` via `python-dotenv` and exposes constants.
- **notebooks/eda_sports.ipynb** — EDA: post counts by source, duplicate detection, sentiment charts, word clouds.

## Dependencies

`requirements.txt` covers core deps. Additional packages used in code but not listed there: `selenium`, `webdriver-manager`, `vaderSentiment`, `seaborn`, `matplotlib`, `wordcloud`.
