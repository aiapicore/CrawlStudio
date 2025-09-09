import time
import asyncio
import tempfile
import json
import sys
from typing import Any, Dict, List, Generator, cast
from urllib.parse import urlparse

import scrapy
from scrapy.http import Response

from .base import CrawlBackend
from ..models import CrawlResult
from ..exceptions import BackendExecutionError


class SimpleSpider(scrapy.Spider):
    name = "simple"

    def __init__(self, url: str, output_file: str | None = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]
        self.output_file = output_file

    def parse(self, response: Response) -> Generator[Dict[str, object], None, None]:
        # Extract data and yield as item
        item: Dict[str, object] = {
            "url": response.url,
            "raw_html": response.text,
            "title": response.css("title::text").get() or "",
            "links": response.css("a::attr(href)").getall(),
            "status_code": response.status,
            "headers": dict(response.headers),
        }
        yield item


class ScrapyBackend(CrawlBackend):
    async def crawl(self, url: str, format: str) -> CrawlResult:
        start = time.time()

        # Use subprocess approach to avoid Twisted reactor conflicts
        try:
            result_data = await self._run_scrapy_subprocess(url)
        except Exception as e:
            raise BackendExecutionError(f"Scrapy crawl failed: {str(e)}")

        if not result_data:
            raise BackendExecutionError("Scrapy returned no results")

        item: Dict[str, object] = result_data[0] if result_data else {}

        # Clean and validate metadata (ensure all values are strings)
        links_list = cast(List[object], item.get("links", []))
        raw_metadata: Dict[str, str] = {
            "title": str(item.get("title", "")),
            "status_code": str(item.get("status_code", "")),
            "url": str(item.get("url", "")),
            "links_count": str(len(links_list)),
        }

        # Filter out None values and ensure all values are strings
        metadata = {}
        for key, value in raw_metadata.items():
            if value is not None:
                metadata[key] = str(value)

        # Scrapy does not support structured data extraction
        structured_data = None

        # Update metadata to include links
        links_list = cast(List[object], item.get("links", []))
        metadata["links"] = json.dumps(links_list)  # Store links in metadata as JSON string

        return CrawlResult(
            url=url,
            backend_used="scrapy",
            markdown=None,  # Scrapy doesn't provide markdown conversion
            raw_html=str(item.get("raw_html", "")),
            structured_data=structured_data,
            metadata=metadata,
            execution_time=time.time() - start,
            cache_hit=False,
        )

    async def _run_scrapy_subprocess(self, url: str) -> list[Dict[str, object]]:
        """Run Scrapy in a subprocess to avoid reactor conflicts"""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as temp_file:
            output_file = temp_file.name

        # Create a simple Scrapy script with proper path handling
        output_file_escaped = output_file.replace('\\', '\\\\')
        scrapy_script = f'''
import sys
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from urllib.parse import urlparse

class SimpleSpider(scrapy.Spider):
    name = "simple"
    start_urls = ["{url}"]
    
    def __init__(self):
        self.allowed_domains = [urlparse("{url}").netloc]
        self.results = []

    def parse(self, response):
        item = {{
            "url": response.url,
            "raw_html": response.text,
            "title": response.css("title::text").get() or "",
            "links": response.css("a::attr(href)").getall(),
            "status_code": response.status,
        }}
        self.results.append(item)
        
        # Write results to file
        with open("{output_file_escaped}", "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

# Configure logging to reduce output
configure_logging({{"LOG_LEVEL": "ERROR"}})

# Run the spider
process = CrawlerProcess({{
    "USER_AGENT": "{self.config.user_agent}",
    "ROBOTSTXT_OBEY": False,
    "LOG_LEVEL": "ERROR",
    "CONCURRENT_REQUESTS": 1,
    "TELNETCONSOLE_ENABLED": False,
}})

process.crawl(SimpleSpider)
process.start()
'''

        # Write script to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as script_file:
            script_file.write(scrapy_script)
            script_path = script_file.name

        try:
            # Run the script as subprocess using current Python executable
            result = await asyncio.create_subprocess_exec(
                sys.executable, script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()

            # Read results from output file
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    results = cast(List[Dict[str, object]], json.load(f))
                return results
            except (FileNotFoundError, json.JSONDecodeError):
                if stderr:
                    raise ValueError(f"Scrapy error: {stderr.decode()}")
                return []

        finally:
            # Clean up temporary files
            try:
                import os
                os.unlink(script_path)
                os.unlink(output_file)
            except Exception:
                pass
