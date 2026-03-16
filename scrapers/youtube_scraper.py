from googleapiclient.discovery import build
from scrapers.base_scraper import BaseScraper
from models.post import Post
from config import YOUTUBE_API_KEY


class YouTubeScraper(BaseScraper):

    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    def get_source_name(self) -> str:
        return "youtube"

    def search(self, keyword: str, limit: int = 10) -> list[Post]:
        posts = []

        response = self.youtube.search().list(
            q=keyword,
            part="snippet",
            maxResults=limit,
            type="video"
        ).execute()

        for item in response.get("items", []):
            post = Post(
                source=self.get_source_name(),
                keyword=keyword,
                title=item["snippet"]["title"],
                text=item["snippet"]["description"],
                url=f"https://youtube.com/watch?v={item['id']['videoId']}",
            )
            posts.append(post)

        return posts