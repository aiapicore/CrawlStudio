#!/usr/bin/env python
"""
Unified test runner for all CrawlStudio backends
Run: python tests/run_all_tests.py
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def run_firecrawl_tests():
    """Run Firecrawl backend tests"""
    print("RUNNING FIRECRAWL TESTS")
    print("=" * 50)
    try:
        from tests.backends.test_firecrawl import run_manual_tests
        await run_manual_tests()
    except Exception as e:
        print(f"Firecrawl tests failed: {e}")
    print()

async def run_crawl4ai_tests():
    """Run Crawl4AI backend tests"""
    print("RUNNING CRAWL4AI TESTS")
    print("=" * 50)
    try:
        from tests.backends.test_crawl4ai import run_manual_tests
        await run_manual_tests()
    except Exception as e:
        print(f"Crawl4AI tests failed: {e}")
    print()

async def run_scrapy_tests():
    """Run Scrapy backend tests"""
    print("RUNNING SCRAPY TESTS")
    print("=" * 50)
    try:
        from tests.backends.test_scrapy import run_manual_tests
        await run_manual_tests()
    except Exception as e:
        print(f"Scrapy tests failed: {e}")
    print()

async def run_comparison_tests():
    """Run backend comparison tests"""
    print("RUNNING BACKEND COMPARISON")
    print("=" * 50)
    try:
        from tests.integration.test_backend_comparison import run_backend_comparison
        await run_backend_comparison()
    except Exception as e:
        print(f"Comparison tests failed: {e}")
    print()

async def main():
    """Run all test suites"""
    print("CrawlStudio Test Suite")
    print("=" * 80)
    print("Testing all backends: Firecrawl, Crawl4AI, Scrapy")
    print("=" * 80)
    
    # Check for required API keys
    missing_keys = []
    if not os.getenv("FIRECRAWL_API_KEY"):
        missing_keys.append("FIRECRAWL_API_KEY")
    
    if missing_keys:
        print("WARNING: Missing API keys:")
        for key in missing_keys:
            print(f"   - {key}")
        print("   Some tests may be skipped.")
        print()
    
    # Run all test suites
    test_suites = [
        ("Firecrawl Backend", run_firecrawl_tests),
        ("Crawl4AI Backend", run_crawl4ai_tests),
        ("Scrapy Backend", run_scrapy_tests),
        ("Backend Comparison", run_comparison_tests)
    ]
    
    results = {}
    for name, test_func in test_suites:
        try:
            print(f"\nStarting {name} tests...")
            await test_func()
            results[name] = "PASSED"
        except KeyboardInterrupt:
            print(f"\n{name} tests interrupted by user")
            results[name] = "INTERRUPTED"
            break
        except Exception as e:
            print(f"\n{name} tests failed: {e}")
            results[name] = "FAILED"
    
    # Print final summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for name, status in results.items():
        status_icon = "PASS" if status == "PASSED" else "FAIL" if status == "FAILED" else "SKIP"
        print(f"[{status_icon}] {name}: {status}")
    
    passed = sum(1 for status in results.values() if status == "PASSED")
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("All tests completed successfully!")
        return 0
    else:
        print("Some tests failed or were skipped")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        sys.exit(1)