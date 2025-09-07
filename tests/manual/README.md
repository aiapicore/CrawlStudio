# Manual Tests

This directory contains development and manual testing scripts used during backend development.

## Files

### Backend-Specific Tests
- `simple_crawl4ai_test.py` - Development test for Crawl4AI backend
- `simple_scrapy_test.py` - Development test for Scrapy backend  
- `simple_test.py` - Quick Firecrawl test
- `test_firecrawl.py` - Original Firecrawl test (has Unicode issues on Windows)

### Comprehensive Tests
- `comprehensive_test.py` - Firecrawl comprehensive testing
- `run_simple_tests.py` - Alternative test runner

## Purpose

These files were created during development to:
- Debug backend issues
- Test individual backends
- Verify fixes and improvements
- Provide quick testing without full test suite

## Usage

Run individual tests:
```bash
python tests/manual/simple_crawl4ai_test.py
python tests/manual/simple_scrapy_test.py
python tests/manual/simple_test.py
```

## Note

For regular testing, use the organized test suite:
```bash
python tests/run_all_tests.py
```

These manual tests are kept for development reference and debugging purposes.