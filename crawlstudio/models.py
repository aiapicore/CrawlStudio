from typing import Dict, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CrawlResult(BaseModel):
    url: str
    backend_used: str
    markdown: Optional[str] = None
    raw_html: Optional[str] = None
    structured_data: Optional[Dict] = None
    metadata: Dict[str, str] = Field(default_factory=dict)
    execution_time: float
    cache_hit: bool = False


class CrawlConfig(BaseSettings):
    firecrawl_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    crawl4ai_api_key: Optional[str] = None
    timeout: int = 30
    user_agent: str = "CrawlStudio/0.1"

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    @property
    def api_keys(self) -> Dict[str, Optional[str]]:
        return {
            "firecrawl": self.firecrawl_api_key,
            "gemini": self.google_api_key,
            "crawl4ai": self.crawl4ai_api_key,
        }
