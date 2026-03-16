from scrapers.youtube_scraper import YouTubeScraper
from scrapers.bbc_scraper import BBCScraper
from db.mongo_handler import MongoHandler

# Test YouTube
print("=== Testing YouTube ===")
yt = YouTubeScraper()
posts = yt.search("NBA finals", limit=3)
for p in posts:
    print(f"Title: {p.title}")
    print(f"URL: {p.url}")
    print("---")

# Test BBC
print("\n=== Testing BBC ===")
bbc = BBCScraper()
posts_bbc = bbc.search("NBA", limit=3)
for p in posts_bbc:
    print(f"Title: {p.title}")
    print("---")

# Test MongoDB
print("\n=== Testing MongoDB ===")
db = MongoHandler()

saved_yt = db.save_many(posts)
print(f"Saved {saved_yt} YouTube posts to MongoDB")

saved_bbc = db.save_many(posts_bbc)
print(f"Saved {saved_bbc} BBC posts to MongoDB")

db.close()
print("Everything works!")