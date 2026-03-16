from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.base_scraper import BaseScraper
from models.post import Post
from config import BBC_SPORT_URL
import time


class BBCScraper(BaseScraper):

    def get_source_name(self) -> str:
        return "bbc"

    def search(self, keyword: str, limit: int = 10) -> list[Post]:
        posts = []

        # פותח Chrome אוטומטית
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # רץ ברקע בלי לפתוח חלון
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        try:
            driver.get("https://www.bbc.co.uk/sport")
            time.sleep(3)

            # מוצא כותרות כתבות
            articles = driver.find_elements(By.TAG_NAME, "h3")

            for article in articles[:limit]:
                title = article.text.strip()
                if title:
                    post = Post(
                        source=self.get_source_name(),
                        keyword=keyword,
                        title=title,
                        text=title,
                        url="https://www.bbc.co.uk/sport"
                    )
                    posts.append(post)

        except Exception as e:
            print(f"BBC scraping error: {e}")
        finally:
            driver.quit()  # סוגר את Chrome תמיד

        return posts