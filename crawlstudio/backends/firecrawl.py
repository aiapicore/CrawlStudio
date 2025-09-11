import time

from firecrawl import Firecrawl

from .base import CrawlBackend
from ..models import CrawlResult
from ..exceptions import ConfigurationError, BackendExecutionError


class FirecrawlBackend(CrawlBackend):
    async def crawl(self, url: str, format: str) -> CrawlResult:
        api_key = self.config.api_keys.get("firecrawl")
        if not api_key:
            raise ConfigurationError("FIRECRAWL_API_KEY is required")

        app = Firecrawl(api_key=api_key)
        start = time.time()

        # Determine output formats based on request
        formats = []
        if format == "markdown":
            formats = ["markdown"]
        elif format == "html":
            formats = ["html", "rawHtml"]  # Try both formats
        elif format == "structured":
            formats = ["markdown", "html", "rawHtml"]
        else:
            formats = ["markdown"]

        # Use the new v3.4.0 API
        try:
            scrape_result = app.scrape(url, formats=formats)
        except Exception as e:
            raise BackendExecutionError(f"Firecrawl scrape failed: {e}")

        # Handle different response structure and check for errors
        if (
            hasattr(scrape_result, "metadata")
            and scrape_result.metadata
            and scrape_result.metadata.error
        ):
            raise BackendExecutionError(f"Firecrawl scrape failed: {scrape_result.metadata.error}")

        # Extract data from the new response format
        if hasattr(scrape_result, "markdown"):
            # New API response object
            data = {
                "markdown": scrape_result.markdown,
                "html": (
                    getattr(scrape_result, "html", None) or getattr(scrape_result, "rawHtml", None)
                ),
                "metadata": (scrape_result.metadata.__dict__ if scrape_result.metadata else {}),
            }
        else:
            # Fallback for dict response
            data = (
                scrape_result
                if isinstance(scrape_result, dict)
                else {"markdown": str(scrape_result)}
            )

        # Handle structured data extraction (simplified for now)
        structured_data = None
        if format == "structured":
            # For now, create basic structured data from markdown
            structured_data = {
                "title": data.get("title", ""),
                "summary": data.get("markdown", "")[:200] + "..." if data.get("markdown") else "",
                "keywords": [],
            }

        # Clean up markdown content if it has the 'markdown=' prefix
        markdown_content = data.get("markdown", "")
        if isinstance(markdown_content, str) and markdown_content.startswith("markdown="):
            markdown_content = markdown_content[9:].strip("'\"")

        # Extract metadata properly and filter out non-string values
        raw_metadata = data.get("metadata", {})
        if not isinstance(raw_metadata, dict):
            raw_metadata = {}

        # Filter metadata to only include string values (Pydantic requirement)
        metadata = {}
        for key, value in raw_metadata.items():
            if isinstance(value, (str, int, float, bool)) and value is not None:
                metadata[key] = str(value)
            elif isinstance(value, str):
                metadata[key] = value

        # Check if we got cached results
        cache_hit = metadata.get("cache_state") == "hit"

        return CrawlResult(
            url=url,
            backend_used="firecrawl",
            markdown=markdown_content,
            raw_html=data.get("html"),
            structured_data=structured_data,
            metadata=metadata,
            execution_time=time.time() - start,
            cache_hit=cache_hit,
        )
