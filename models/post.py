from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Post:
    source: str          
    keyword: str         
    title: str           
    text: str            
    url: str             
    date: datetime = field(default_factory=datetime.now)
    sentiment: float = 0.0
    likes: int = 0

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "keyword": self.keyword,
            "title": self.title,
            "text": self.text,
            "url": self.url,
            "date": self.date,
            "sentiment": self.sentiment,
            "likes": self.likes
        }