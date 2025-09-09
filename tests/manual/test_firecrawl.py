"""
Test script for Firecrawl backend integration
Run: python test_firecrawl.py
"""
import asyncio
import os
import pytest
from dotenv import load_dotenv
from crawlstudio import CrawlConfig, FirecrawlBackend

load_dotenv()


@pytest.mark.asyncio
async def test_basic_scrape():
    """Test basic URL scraping with markdown format"""
    print("Testing Firecrawl Basic Scrape...")

    config = CrawlConfig()
    if not config.firecrawl_api_key:
        print("❌ FIRECRAWL_API_KEY not found in .env file")
        return False

    backend = FirecrawlBackend(config)

    try:
        result = await backend.crawl("https://nccs-website.vercel.app/", format="markdown")
        print(f"✅ Success: {result.backend_used}")
        print(f"⏱️ Execution time: {result.execution_time:.2f}s")
        print(f"📄 Markdown length: {len(result.markdown) if result.markdown else 0}")
        print(f"🔗 URL: {result.url}")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_structured_extraction():
    """Test structured data extraction"""
    print("Testing Firecrawl Structured Extraction...")

    config = CrawlConfig()
    backend = FirecrawlBackend(config)

    try:
        result = await backend.crawl("https://news.ycombinator.com", format="structured")
        print(f"✅ Success: {result.backend_used}")
        print(f"⏱️ Execution time: {result.execution_time:.2f}s")
        print(f"🧠 Structured data: {result.structured_data}")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_html_extraction():
    """Test raw HTML extraction"""
    print("Testing Firecrawl HTML Extraction...")

    config = CrawlConfig()
    backend = FirecrawlBackend(config)

    try:
        result = await backend.crawl("https://httpbin.org/html", format="html")
        print(f"✅ Success: {result.backend_used}")
        print(f"⏱️ Execution time: {result.execution_time:.2f}s")
        print(f"📄 HTML length: {len(result.raw_html) if result.raw_html else 0}")
        print(f"🔗 Metadata: {result.metadata}")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling with invalid URL"""
    print("Testing Error Handling...")

    config = CrawlConfig()
    backend = FirecrawlBackend(config)

    try:
        # Test with a truly malformed URL that should fail
        result = await backend.crawl("not-a-valid-url-at-all", format="markdown")
        print(f"⚠️ Unexpected success: {result}")
        return False
    except Exception as e:
        print(f"✅ Expected error caught: {str(e)}")
        print("=" * 50)
        return True


async def main():
    """Run all tests"""
    print("Starting Firecrawl Backend Tests\n")

    tests = [
        test_basic_scrape,
        test_structured_extraction,
        test_html_extraction,
        test_error_handling
    ]

    results = []
    for test in tests:
        result = await test()
        results.append(result)
        print()

    passed = sum(results)
    total = len(results)

    print(f"📊 Test Results: {passed}/{total} passed")
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    asyncio.run(main())
