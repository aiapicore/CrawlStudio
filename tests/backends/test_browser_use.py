"""
Comprehensive tests for Browser-Use backend
"""
import asyncio
import pytest
from dotenv import load_dotenv
from crawlstudio import CrawlConfig, BrowserUseBackend

load_dotenv()

class TestBrowserUseBackend:
    
    @pytest.fixture
    def backend(self):
        """Create Browser-Use backend instance"""
        config = CrawlConfig()
        return BrowserUseBackend(config)
    
    @pytest.mark.asyncio
    async def test_dependency_check(self):
        """Test that dependencies are properly checked"""
        config = CrawlConfig()
        try:
            backend = BrowserUseBackend(config)
            # If no exception, dependencies are available
            assert True
        except ValueError as e:
            # Expected if browser-use or AI keys not available
            assert "browser-use" in str(e) or "API key" in str(e)
    
    @pytest.mark.asyncio 
    @pytest.mark.skipif(not _has_browser_use_deps(), reason="browser-use not installed")
    async def test_markdown_extraction(self, backend):
        """Test AI-driven markdown extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="markdown")
        
        assert result.backend_used == "browser-use"
        assert result.url == "https://httpbin.org/html"
        assert result.markdown is not None
        assert result.execution_time > 0
        assert "ai_backend" in result.metadata
        
    @pytest.mark.asyncio
    @pytest.mark.skipif(not _has_browser_use_deps(), reason="browser-use not installed") 
    async def test_structured_extraction(self, backend):
        """Test AI-driven structured data extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="structured")
        
        assert result.backend_used == "browser-use"
        assert result.structured_data is not None
        assert "title" in result.structured_data
        assert "summary" in result.structured_data
        assert "keywords" in result.structured_data
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(not _has_browser_use_deps(), reason="browser-use not installed")
    async def test_html_extraction(self, backend):
        """Test AI-driven HTML extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="html")
        
        assert result.backend_used == "browser-use"
        assert result.raw_html is not None
        assert len(result.raw_html) > 0


def _has_browser_use_deps() -> bool:
    """Check if browser-use dependencies are available"""
    try:
        import browser_use
        import os
        return bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    except ImportError:
        return False


async def run_manual_tests():
    """Manual test runner for Browser-Use backend"""
    print("="*60)
    print("BROWSER-USE BACKEND TESTS")
    print("="*60)
    
    # Check dependencies first
    if not _has_browser_use_deps():
        print("SKIPPING: browser-use not installed or no AI API key")
        print("To test browser-use backend:")
        print("1. pip install browser-use")
        print("2. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        print("3. uvx playwright install chromium --with-deps")
        return
    
    config = CrawlConfig()
    backend = BrowserUseBackend(config)
    test_url = "https://httpbin.org/html"
    
    # Test 1: AI-driven markdown extraction
    print("\n1. Testing AI MARKDOWN extraction...")
    try:
        result = await backend.crawl(test_url, format="markdown")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s (AI processing)")
        print(f"   Markdown: {len(result.markdown) if result.markdown else 0} chars")
        print(f"   AI Backend: {result.metadata.get('ai_backend', 'N/A')}")
    except Exception as e:
        print(f"   FAILED: {e}")
    
    # Test 2: AI-driven structured extraction
    print("\n2. Testing AI STRUCTURED extraction...")
    try:
        result = await backend.crawl(test_url, format="structured")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        if result.structured_data:
            print(f"   Title: {result.structured_data.get('title', 'N/A')}")
            print(f"   Keywords: {len(result.structured_data.get('keywords', []))} found")
            print(f"   Summary length: {len(result.structured_data.get('summary', ''))}")
    except Exception as e:
        print(f"   FAILED: {e}")
    
    # Test 3: AI-driven HTML extraction  
    print("\n3. Testing AI HTML extraction...")
    try:
        result = await backend.crawl(test_url, format="html")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   HTML: {len(result.raw_html) if result.raw_html else 0} chars")
    except Exception as e:
        print(f"   FAILED: {e}")
    
    # Test 4: Different website
    print("\n4. Testing different website...")
    try:
        result = await backend.crawl("https://example.com", format="structured")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        if result.structured_data:
            print(f"   AI extracted title: {result.structured_data.get('title', 'N/A')[:50]}...")
    except Exception as e:
        print(f"   FAILED: {e}")
    
    print("\n" + "="*60)
    print("BROWSER-USE TESTS COMPLETE")
    print("Note: This backend uses AI agents for intelligent web interaction!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_manual_tests())