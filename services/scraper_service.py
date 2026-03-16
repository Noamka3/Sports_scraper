from scrapers.base_scraper import BaseScraper
from db.mongo_handler import MongoHandler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class ScraperService:

    def __init__(self, scraper: BaseScraper, db: MongoHandler):
        self.scraper = scraper
        self.db = db
        self.analyzer = SentimentIntensityAnalyzer()

    def search_and_analyze(self, keyword: str, limit: int = 10) -> list:
        # Step 1 — fetch data from source
        posts = self.scraper.search(keyword, limit)

        # Step 2 — run sentiment on each post
        for post in posts:
            score = self.analyzer.polarity_scores(post.title)
            post.sentiment = score["compound"]

        return posts

    def save_posts(self, posts: list) -> int:
        return self.db.save_many(posts)

    def search_save_analyze(self, keyword: str, limit: int = 10) -> list:
        posts = self.search_and_analyze(keyword, limit)
        self.save_posts(posts)
        return posts

    def get_by_source(self, source: str) -> list:
        return self.db.get_by_source(source)

    def get_by_keyword(self, keyword: str) -> list:
        return self.db.get_by_keyword(keyword)
