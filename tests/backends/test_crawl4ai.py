"""
Comprehensive tests for Crawl4AI backend
"""
import asyncio
import pytest
from dotenv import load_dotenv
from crawlstudio import CrawlConfig, Crawl4AIBackend
from crawlstudio.exceptions import BackendExecutionError

load_dotenv()


class TestCrawl4AIBackend:

    @pytest.fixture
    def backend(self):
        """Create Crawl4AI backend instance"""
        config = CrawlConfig()
        return Crawl4AIBackend(config)

    @pytest.mark.asyncio
    async def test_basic_markdown_crawling(self, backend):
        """Test basic markdown extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="markdown")

        assert result.backend_used == "crawl4ai"
        assert result.url == "https://httpbin.org/html"
        assert result.markdown is not None
        assert len(result.markdown) > 0
        assert result.execution_time > 0

    @pytest.mark.asyncio
    async def test_html_extraction(self, backend):
        """Test HTML extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="html")

        assert result.backend_used == "crawl4ai"
        assert result.raw_html is not None
        assert len(result.raw_html) > 0
        assert "<html" in result.raw_html.lower()

    @pytest.mark.asyncio
    async def test_structured_extraction_without_api_key(self, backend):
        """Test structured extraction fallback without API key"""
        result = await backend.crawl("https://httpbin.org/html", format="structured")

        assert result.backend_used == "crawl4ai"
        assert result.structured_data is not None
        assert "title" in result.structured_data
        assert "summary" in result.structured_data
        assert "keywords" in result.structured_data

    @pytest.mark.asyncio
    async def test_error_handling_invalid_url(self, backend):
        """Test error handling with invalid URL"""
        with pytest.raises(BackendExecutionError, match="Crawl4AI backend error"):
            await backend.crawl("not-a-valid-url", format="markdown")

    @pytest.mark.asyncio
    async def test_different_websites(self, backend):
        """Test crawling different websites"""
        test_urls = [
            "https://example.com",
            "https://httpbin.org/html"
        ]

        for url in test_urls:
            result = await backend.crawl(url, format="markdown")
            assert result.backend_used == "crawl4ai"
            assert result.markdown is not None
            assert len(result.markdown) > 0


async def run_manual_tests():
    """Manual test runner"""
    print("="*60)
    print("CRAWL4AI BACKEND TESTS")
    print("="*60)

    config = CrawlConfig()
    backend = Crawl4AIBackend(config)
    test_url = "https://httpbin.org/html"

    # Test 1: Markdown format
    print("\n1. Testing MARKDOWN format...")
    try:
        result = await backend.crawl(test_url, format="markdown")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Markdown: {len(result.markdown)} chars")
        print(f"   HTML: {len(result.raw_html) if result.raw_html else 0} chars")
        print(f"   Cache hit: {result.cache_hit}")
        print(f"   Metadata keys: {list(result.metadata.keys())}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 2: HTML format
    print("\n2. Testing HTML format...")
    try:
        result = await backend.crawl(test_url, format="html")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Markdown: {len(result.markdown) if result.markdown else 0} chars")
        print(f"   HTML: {len(result.raw_html) if result.raw_html else 0} chars")
        print(f"   Cache hit: {result.cache_hit}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 3: Structured format
    print("\n3. Testing STRUCTURED format...")
    try:
        result = await backend.crawl(test_url, format="structured")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Structured data: {result.structured_data}")
        print(f"   Cache hit: {result.cache_hit}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 4: Error handling
    print("\n4. Testing ERROR handling...")
    try:
        result = await backend.crawl("invalid-url-format", format="markdown")
        print(f"   UNEXPECTED SUCCESS: {result}")
    except Exception as e:
        print(f"   SUCCESS: Error properly caught - {str(e)[:100]}...")

    # Test 5: Real website
    print("\n5. Testing real website...")
    try:
        result = await backend.crawl("https://example.com", format="markdown")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Markdown: {len(result.markdown)} chars")
        print(f"   Has HTML: {result.raw_html is not None}")
    except Exception as e:
        print(f"   FAILED: {e}")

    print("\n" + "="*60)
    print("CRAWL4AI TESTS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_manual_tests())
