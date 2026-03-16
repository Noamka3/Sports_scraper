from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def search(self, keyword: str, limit: int) -> list:
        """מחפש לפי מילת מפתח, מחזיר רשימת Post"""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """מחזיר את שם המקור — youtube / bbc"""
        pass