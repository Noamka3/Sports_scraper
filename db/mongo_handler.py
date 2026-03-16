from pymongo import MongoClient
from models.post import Post
from config import MONGO_URI, MONGO_DB_NAME


class MongoHandler:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.collection = self.db["posts"]

    def save_post(self, post: Post) -> bool:
        try:
            self.collection.insert_one(post.to_dict())
            return True
        except Exception as e:
            print(f"Error saving post: {e}")
            return False

    def save_many(self, posts: list[Post]) -> int:
        try:
            dicts = [p.to_dict() for p in posts]
            result = self.collection.insert_many(dicts)
            return len(result.inserted_ids)
        except Exception as e:
            print(f"Error saving posts: {e}")
            return 0

    def get_by_source(self, source: str) -> list:
        return list(self.collection.find({"source": source}))

    def get_by_keyword(self, keyword: str) -> list:
        return list(self.collection.find({"keyword": keyword}))

    def get_all(self) -> list:
        return list(self.collection.find())

    def close(self):
        self.client.close()