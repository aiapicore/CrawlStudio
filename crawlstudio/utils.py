from typing import Any
from diskcache import Cache
import aiohttp
from urllib.parse import urlparse, urljoin

cache = Cache("crawlstudio_cache")


async def check_robots_txt(url: str, user_agent: str) -> bool:
    # Placeholder for robots.txt parsing
    # TODO: Implement actual parsing using robotparser
    robots_url = urljoin(url, "/robots.txt")
    async with aiohttp.ClientSession() as session:
        async with session.get(robots_url) as response:
            if response.status == 200:
                # Simulate check
                return True
    return True  # Default allow


async def is_js_heavy(url: str) -> bool:
    # Placeholder for JS detection
    # TODO: Check headers or content for JS indicators
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            content_type = response.headers.get("Content-Type", "")
            return "javascript" in content_type.lower()
    return False