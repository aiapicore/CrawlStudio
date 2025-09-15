"""
Simple test runner without pytest dependencies
"""
import asyncio
from crawlstudio import CrawlConfig, FirecrawlBackend, Crawl4AIBackend, ScrapyBackend


async def test_all_backends():
    print("=" * 80)
    print("CRAWLSTUDIO BACKEND COMPARISON")
    print("=" * 80)

    config = CrawlConfig()
    test_url = "https://example.com/"

    # Initialize backends
    backends = {
        "Firecrawl": FirecrawlBackend(config),
        "Crawl4AI": Crawl4AIBackend(config),
        "Scrapy": ScrapyBackend(config)
    }

    formats = ["markdown", "html", "structured"]

    for format_type in formats:
        print(f"\n{format_type.upper()} FORMAT COMPARISON")
        print("-" * 60)
        print(f"{'Backend':<12} | {'Time':<8} | {'Content':<12} | {'Status':<15}")
        print("-" * 60)

        for name, backend in backends.items():
            try:
                result = await backend.crawl(test_url, format=format_type)

                # Calculate content length
                content_length = 0
                if format_type == "markdown" and result.markdown:
                    content_length = len(result.markdown)
                elif format_type == "html" and result.raw_html:
                    content_length = len(result.raw_html)
                elif format_type == "structured" and result.structured_data:
                    content_length = len(str(result.structured_data))

                status = "SUCCESS"
                if content_length == 0 and format_type == "markdown":
                    status = "NO_MARKDOWN"
                elif content_length == 0 and format_type == "html":
                    status = "NO_HTML"
                elif content_length == 0 and format_type == "structured":
                    status = "NO_STRUCTURED"

                print(f"{name:<12} | {result.execution_time:6.2f}s | {content_length:8,} ch | {status:<15}")

            except Exception as e:
                error_msg = str(e)[:30] + "..." if len(str(e)) > 30 else str(e)
                print(f"{name:<12} | {'ERROR':<8} | {'0':<12} | {error_msg:<15}")

    print("\n" + "=" * 80)
    print("INDIVIDUAL BACKEND TESTS")
    print("=" * 80)

    # Test each backend individually
    for name, backend in backends.items():
        print(f"\nTesting {name} Backend:")
        print("-" * 40)

        try:
            # Basic functionality test
            result = await backend.crawl(test_url, format="markdown")
            print(f"  ✓ Basic crawling: SUCCESS ({result.execution_time:.2f}s)")

            if result.markdown:
                print(f"  ✓ Markdown: {len(result.markdown)} characters")
            else:
                print(f"  - Markdown: Not supported")

            if result.raw_html:
                print(f"  ✓ HTML: {len(result.raw_html)} characters")
            else:
                print(f"  - HTML: Not available")

            if result.metadata:
                print(f"  ✓ Metadata: {len(result.metadata)} fields")
            else:
                print(f"  - Metadata: None")

            print(f"  ✓ Cache detection: {'Enabled' if result.cache_hit else 'Disabled'}")

        except Exception as e:
            print(f"  ✗ ERROR: {str(e)[:60]}...")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("Backend Capabilities:")
    print("- Firecrawl: ✓ Markdown, ✓ HTML, ✓ Structured, ✓ Caching")
    print("- Crawl4AI:  ✓ Markdown, ✓ HTML, ✓ Structured, ~ Caching")
    print("- Scrapy:    - Markdown, ✓ HTML, - Structured, - Caching")

    print("\nRecommended Usage:")
    print("- Best overall: Firecrawl (requires API key)")
    print("- Local/Free:   Crawl4AI (slower but comprehensive)")
    print("- HTML only:    Scrapy (fast, minimal dependencies)")

if __name__ == "__main__":
    asyncio.run(test_all_backends())
