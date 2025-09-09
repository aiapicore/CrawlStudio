import time
import os
import sys

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai import LLMExtractionStrategy, LLMConfig

from .base import CrawlBackend
from ..models import CrawlResult
from ..exceptions import BackendExecutionError


class Crawl4AIBackend(CrawlBackend):
    async def crawl(self, url: str, format: str) -> CrawlResult:
        start = time.time()
        api_key = self.config.api_keys.get("crawl4ai")  # Optional for LLM extraction

        # Configure browser settings for Windows compatibility (kept for future use)
        # BrowserConfig is configured implicitly in AsyncWebCrawler

        # Configure crawler run settings - disable cache to avoid Windows Unicode issues
        run_config = CrawlerRunConfig(cache_mode=CacheMode.DISABLED, word_count_threshold=10)

        # Set up extraction strategy for structured data
        extraction_strategy = None
        if format == "structured" and api_key:
            try:
                # Configure LLM for extraction
                llm_config = LLMConfig(provider="openai/gpt-4o-mini", api_token=api_key)

                extraction_strategy = LLMExtractionStrategy(
                    llm_config=llm_config,
                    schema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Page title"},
                            "summary": {"type": "string", "description": "Page summary"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Key topics",
                            },
                        },
                    },
                    extraction_type="schema",
                    instruction=(
                        "Extract the title, a brief summary, and key topics from this webpage."
                    ),
                )
                run_config.extraction_strategy = extraction_strategy
            except Exception:
                # Fallback if LLM config fails
                # Log or ignore; fallback to non-LLM flow
                pass

        try:
            # Temporarily redirect stdout to handle Unicode issues on Windows
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            # Use minimal configuration to avoid Windows Unicode issues
            with open(os.devnull, "w", encoding="utf-8") as devnull:
                sys.stdout = devnull
                sys.stderr = devnull

                async with AsyncWebCrawler(headless=True, verbose=False) as crawler:
                    result = await crawler.arun(
                        url=url,
                        word_count_threshold=10,
                        bypass_cache=True,  # Avoid cache Unicode issues
                        extraction_strategy=(
                            extraction_strategy if format == "structured" and api_key else None
                        ),
                    )

            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Handle successful crawling
            if result.success:
                # Extract structured data
                structured_data = None
                if format == "structured" and result.extracted_content:
                    structured_data = result.extracted_content
                elif format == "structured":
                    # Fallback structured data from markdown
                    structured_data = {
                        "title": getattr(result, "title", ""),
                        "summary": result.markdown[:200] + "..." if result.markdown else "",
                        "keywords": [],
                    }

                # Filter metadata to only include string values
                metadata = {}
                if hasattr(result, "metadata") and result.metadata:
                    for key, value in result.metadata.items():
                        if isinstance(value, (str, int, float, bool)) and value is not None:
                            metadata[key] = str(value)

                return CrawlResult(
                    url=url,
                    backend_used="crawl4ai",
                    markdown=result.markdown,
                    raw_html=result.html,
                    structured_data=structured_data,
                    metadata=metadata,
                    execution_time=time.time() - start,
                    cache_hit=getattr(result, "from_cache", False),
                )
            else:
                raise BackendExecutionError(
                    f"Crawl4AI failed: {getattr(result, 'error_message', 'Unknown error')}"
                )

        except Exception as e:
            # Restore stdout/stderr in case of error
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            raise BackendExecutionError(f"Crawl4AI backend error: {str(e)}")
