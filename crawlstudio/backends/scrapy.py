import time
import asyncio
import subprocess
import tempfile
import json
import sys
from typing import Dict, Any, Optional
from urllib.parse import urlparse

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from twisted.internet.asyncioreactor import AsyncioSelectorReactor

from .base import CrawlBackend
from ..models import CrawlConfig, CrawlResult


class SimpleSpider(scrapy.Spider):
    name = "simple"
    
    def __init__(self, url: str, output_file: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]
        self.output_file = output_file

    def parse(self, response):
        # Extract data and yield as item
        item = {
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
            raise ValueError(f"Scrapy crawl failed: {str(e)}")

        if not result_data:
            raise ValueError("Scrapy returned no results")

        item = result_data[0] if result_data else {}

        # Clean and validate metadata (ensure all values are strings)
        raw_metadata = {
            "title": item.get("title", ""),
            "status_code": str(item.get("status_code", "")),
            "url": item.get("url", ""),
            "links_count": str(len(item.get("links", []))),
        }
        
        # Filter out None values and ensure all values are strings
        metadata = {}
        for key, value in raw_metadata.items():
            if value is not None:
                metadata[key] = str(value)

        # Simple structured data extraction if requested
        structured_data = None
        if format == "structured":
            structured_data = {
                "title": item.get("title", ""),
                "summary": item.get("raw_html", "")[:200] + "..." if item.get("raw_html") else "",
                "keywords": [],
                "links": item.get("links", [])[:5]  # First 5 links
            }

        return CrawlResult(
            url=url,
            backend_used="scrapy",
            markdown=None,  # Scrapy doesn't provide markdown conversion
            raw_html=item.get("raw_html", ""),
            structured_data=structured_data,
            metadata=metadata,
            execution_time=time.time() - start,
            cache_hit=False,
        )

    async def _run_scrapy_subprocess(self, url: str) -> list[Dict]:
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
                    results = json.load(f)
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
            except:
                pass