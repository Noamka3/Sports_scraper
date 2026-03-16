from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

BBC_SPORT_URL = "https://www.bbc.com/sport"
SEARCH_LIMIT = 10