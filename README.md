# Sports Scraper 🏀⚽

An application for collecting sports data from YouTube and BBC Sport, storing it in MongoDB, and performing EDA analysis.

---

## Prerequisites

- Python 3.8+
- MongoDB installed and running as a service
- Chrome Browser installed
- YouTube Data API v3 Key

---

## Installation

### 1. Clone the project
```bash
git clone <repo-url>
cd sports_scraper
```

### 2. Install all packages
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file in the root directory
```
YOUTUBE_API_KEY=your_api_key_here
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=sports_scraper
```

### 4. Start MongoDB
```bash
net start MongoDB
```

### 5. Run the application
```bash
python gui/app.py
```

---

## Project Structure

```
sports_scraper/
├── .env                         ← API Keys (not uploaded to GitHub!)
├── .gitignore
├── config.py                    ← Reads from .env
├── requirements.txt
├── models/
│   └── post.py                  ← Unified data model
├── scrapers/
│   ├── base_scraper.py          ← Abstract Base Class
│   ├── youtube_scraper.py       ← YouTube API v3
│   └── bbc_scraper.py           ← Selenium + BeautifulSoup
├── db/
│   └── mongo_handler.py         ← MongoDB save & retrieve
├── services/
│   └── scraper_service.py       ← Business Logic + Sentiment
├── gui/
│   └── app.py                   ← Tkinter GUI
└── notebooks/
    └── eda_sports.ipynb         ← EDA + Data Analysis
```

---

## Using the Application

1. Launch the application with `python gui/app.py`
2. Enter a search keyword (e.g., `NBA finals`)
3. Select a source — YouTube or BBC Sport
4. Click **Search** to view results
5. Click **Save** to save to MongoDB
6. Click **Load** to retrieve saved data with filters

---

## EDA Analysis

```bash
jupyter notebook notebooks/eda_sports.ipynb
```

---

## requirements.txt

```
PySimpleGUI
google-api-python-client
selenium
webdriver-manager
pymongo
beautifulsoup4
requests
vaderSentiment
pandas
matplotlib
seaborn
wordcloud
notebook
python-dotenv
```

---

## Notes

- The `.env` file is not uploaded to GitHub — keep your API Key safe
- ChromeDriver is installed automatically via `webdriver-manager`
- MongoDB must be running before launching the application
