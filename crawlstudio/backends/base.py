from abc import ABC, abstractmethod
from ..models import CrawlConfig, CrawlResult


class CrawlBackend(ABC):
    def __init__(self, config: CrawlConfig):
        self.config = config

    @abstractmethod
    async def crawl(self, url: str, format: str) -> CrawlResult:
        pass