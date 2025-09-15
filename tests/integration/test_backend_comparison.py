"""
Integration tests comparing all backends
"""
import asyncio
import pytest
from dotenv import load_dotenv
from crawlstudio import CrawlConfig, FirecrawlBackend, Crawl4AIBackend, ScrapyBackend

load_dotenv()


class TestBackendComparison:

    @pytest.fixture
    def config(self):
        return CrawlConfig()

    @pytest.fixture
    def all_backends(self, config):
        return {
            "firecrawl": FirecrawlBackend(config),
            "crawl4ai": Crawl4AIBackend(config),
            "scrapy": ScrapyBackend(config)
        }

    @pytest.mark.asyncio
    async def test_markdown_support_comparison(self, all_backends):
        """Compare markdown support across backends"""
        url = "https://example.com/"
        results = {}

        for name, backend in all_backends.items():
            try:
                result = await backend.crawl(url, format="markdown")
                results[name] = {
                    "success": True,
                    "markdown_length": len(result.markdown) if result.markdown else 0,
                    "execution_time": result.execution_time
                }
            except Exception as e:
                results[name] = {"success": False, "error": str(e)}

        # Firecrawl and Crawl4AI should support markdown
        if "firecrawl" in results and results["firecrawl"]["success"]:
            assert results["firecrawl"]["markdown_length"] > 0

        if "crawl4ai" in results and results["crawl4ai"]["success"]:
            assert results["crawl4ai"]["markdown_length"] > 0

        # Scrapy might not support markdown conversion
        print(f"Results: {results}")

    @pytest.mark.asyncio
    async def test_html_support_comparison(self, all_backends):
        """Compare HTML extraction across backends"""
        url = "https://example.com/"
        results = {}

        for name, backend in all_backends.items():
            try:
                result = await backend.crawl(url, format="html")
                results[name] = {
                    "success": True,
                    "html_length": len(result.raw_html) if result.raw_html else 0,
                    "execution_time": result.execution_time
                }
            except Exception as e:
                results[name] = {"success": False, "error": str(e)}

        # All backends should support HTML extraction
        for name, result in results.items():
            if result["success"]:
                assert result["html_length"] > 0, f"{name} should extract HTML"

    @pytest.mark.asyncio
    async def test_performance_comparison(self, all_backends):
        """Compare performance across backends"""
        url = "https://example.com/"
        performance_results = {}

        for name, backend in all_backends.items():
            times = []
            for _ in range(2):  # Run twice to account for caching
                try:
                    result = await backend.crawl(url, format="markdown")
                    times.append(result.execution_time)
                except Exception:
                    continue

            if times:
                performance_results[name] = {
                    "avg_time": sum(times) / len(times),
                    "min_time": min(times),
                    "max_time": max(times)
                }

        print(f"Performance comparison: {performance_results}")
        assert len(performance_results) > 0


async def run_backend_comparison():
    """Manual backend comparison runner"""
    print("="*80)
    print("BACKEND COMPARISON TEST")
    print("="*80)

    config = CrawlConfig()
    backends = {
        "firecrawl": FirecrawlBackend(config),
        "crawl4ai": Crawl4AIBackend(config),
        "scrapy": ScrapyBackend(config)
    }

    test_url = "https://example.com/"
    formats = ["markdown", "html", "structured"]

    for format_type in formats:
        print(f"\n{format_type.upper()} FORMAT COMPARISON")
        print("-" * 40)

        for name, backend in backends.items():
            try:
                result = await backend.crawl(test_url, format=format_type)

                content_length = 0
                if format_type == "markdown" and result.markdown:
                    content_length = len(result.markdown)
                elif format_type == "html" and result.raw_html:
                    content_length = len(result.raw_html)
                elif format_type == "structured" and result.structured_data:
                    content_length = len(str(result.structured_data))

                print(
                    f"{name:12} | {result.execution_time:6.2f}s | {content_length:8,} chars | Cache: {result.cache_hit}")

            except Exception as e:
                print(f"{name:12} | ERROR: {str(e)[:50]}...")

    print("\n" + "="*80)
    print("PERFORMANCE SUMMARY")
    print("="*80)

    # Performance test
    performance_results = {}
    for name, backend in backends.items():
        try:
            # Test 3 times for average
            times = []
            for i in range(3):
                result = await backend.crawl(test_url, format="markdown")
                times.append(result.execution_time)

            performance_results[name] = {
                "avg": sum(times) / len(times),
                "min": min(times),
                "max": max(times)
            }
        except Exception as e:
            performance_results[name] = {"error": str(e)[:50]}

    for name, stats in performance_results.items():
        if "error" in stats:
            print(f"{name:12} | ERROR: {stats['error']}")
        else:
            print(
                f"{name:12} | Avg: {stats['avg']:.2f}s | Min: {stats['min']:.2f}s | Max: {stats['max']:.2f}s")


if __name__ == "__main__":
    asyncio.run(run_backend_comparison())
