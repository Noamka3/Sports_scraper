# Sports Scraper 🏀⚽

אפליקציה לאיסוף נתוני ספורט מ-YouTube ו-BBC Sport, שמירה ב-MongoDB וניתוח EDA.

---

## דרישות מקדימות

- Python 3.8+
- MongoDB מותקן ורץ כ-Service
- Chrome Browser מותקן
- YouTube Data API v3 Key

---

## התקנה

### 1. שכפל את הפרויקט
```bash
git clone <repo-url>
cd sports_scraper
```

### 2. התקן את כל החבילות
```bash
pip install -r requirements.txt
```

### 3. צור קובץ `.env` בתיקייה הראשית
```
YOUTUBE_API_KEY=your_api_key_here
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=sports_scraper
```

### 4. הפעל את MongoDB
```bash
net start MongoDB
```

### 5. הרץ את האפליקציה
```bash
python gui/app.py
```

---

## מבנה הפרויקט

```
sports_scraper/
├── .env                         ← API Keys (לא מועלה ל-GitHub!)
├── .gitignore
├── config.py                    ← קורא מה-.env
├── requirements.txt
├── models/
│   └── post.py                  ← מודל נתונים אחיד
├── scrapers/
│   ├── base_scraper.py          ← Abstract Base Class
│   ├── youtube_scraper.py       ← YouTube API v3
│   └── bbc_scraper.py           ← Selenium + BeautifulSoup
├── db/
│   └── mongo_handler.py         ← שמירה ואחזור MongoDB
├── services/
│   └── scraper_service.py       ← Business Logic + Sentiment
├── gui/
│   └── app.py                   ← PySimpleGUI
└── notebooks/
    └── eda_sports.ipynb         ← EDA + ניתוח נתונים
```

---

## שימוש באפליקציה

1. פתח את האפליקציה עם `python gui/app.py`
2. הכנס מילת חיפוש (לדוגמה: `NBA finals`)
3. בחר מקור — YouTube או BBC Sport
4. לחץ **Search** לראות תוצאות
5. לחץ **Save** לשמור ל-MongoDB
6. לחץ **Load** לאחזר נתונים שמורים עם פילטרים

---

## ניתוח EDA

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

## הערות

- קובץ `.env` לא מועלה ל-GitHub — שמור את ה-API Key בטוח
- ChromeDriver מותקן אוטומטית דרך `webdriver-manager`
- MongoDB חייב לרוץ לפני הפעלת האפליקציה
