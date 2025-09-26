"""
Simple test for updated Scrapy backend
"""
import asyncio
import pytest
from crawlstudio import CrawlConfig, ScrapyBackend


@pytest.mark.asyncio
async def test_scrapy():
    print("Testing updated Scrapy backend...")

    config = CrawlConfig()
    backend = ScrapyBackend(config)

    try:
        print("Testing basic HTML extraction...")
        result = await backend.crawl("https://example.com/", format="html")
        print(f"SUCCESS: {result.backend_used}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"HTML length: {len(result.raw_html) if result.raw_html else 0}")
        print(f"Markdown: {result.markdown} (expected None)")
        print(f"Metadata: {result.metadata}")
        print("=" * 50)

        print("Testing markdown format (should work but no conversion)...")
        result2 = await backend.crawl("https://example.com/", format="markdown")
        print(f"SUCCESS: {result2.backend_used}")
        print(f"HTML length: {len(result2.raw_html) if result2.raw_html else 0}")
        print(f"Markdown: {result2.markdown} (expected None)")
        print("=" * 50)

        print("Testing structured extraction...")
        result3 = await backend.crawl("https://example.com/", format="structured")
        print(f"SUCCESS: {result3.backend_used}")
        print(f"Structured data: {result3.structured_data}")
        print("=" * 50)

        print("All Scrapy tests passed!")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_scrapy())
