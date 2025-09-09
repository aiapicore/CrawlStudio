import argparse
import asyncio
import sys
from typing import Optional

from .models import CrawlConfig
from .backends import (
    FirecrawlBackend,
    Crawl4AIBackend,
    ScrapyBackend,
    BrowserUseBackend,
)
from .exceptions import (
    ConfigurationError,
    DependencyMissingError,
    BackendExecutionError,
    CrawlError,
)


BACKENDS = {
    "firecrawl": FirecrawlBackend,
    "crawl4ai": Crawl4AIBackend,
    "scrapy": ScrapyBackend,
    "browser-use": BrowserUseBackend,
}


async def _run(args: argparse.Namespace) -> int:
    backend_name: str = args.backend
    url: str = args.url
    output_format: str = args.format

    if backend_name not in BACKENDS:
        print(f"Unknown backend: {backend_name}. Choose from: {', '.join(BACKENDS.keys())}")
        return 2

    backend_cls = BACKENDS[backend_name]
    config = CrawlConfig()

    try:
        # mypy: backend_cls is a concrete subclass chosen from BACKENDS
        backend = backend_cls(config)  # type: ignore[abstract]
        result = await backend.crawl(url, output_format)
    except (ConfigurationError, DependencyMissingError) as e:
        print(f"Configuration error: {e}")
        return 2
    except BackendExecutionError as e:
        print(f"Backend error: {e}")
        return 1
    except CrawlError as e:
        print(f"Crawl error: {e}")
        return 1

    if args.print == "markdown" and result.markdown is not None:
        print(result.markdown)
    elif args.print == "html" and result.raw_html is not None:
        print(result.raw_html)
    elif args.print == "structured" and result.structured_data is not None:
        import json

        print(json.dumps(result.structured_data, ensure_ascii=False, indent=2))
    else:
        # Default summary output
        print(f"URL: {result.url}")
        print(f"Backend: {result.backend_used}")
        print(f"Format requested: {output_format}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Cache hit: {result.cache_hit}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crawlstudio", description="Unified CLI for CrawlStudio backends"
    )
    parser.add_argument("url", help="Target URL to crawl")
    parser.add_argument(
        "--backend",
        default="firecrawl",
        choices=list(BACKENDS.keys()),
        help="Backend to use",
    )
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "html", "structured"],
        help="Output format",
    )
    parser.add_argument(
        "--print",
        dest="print",
        choices=["summary", "markdown", "html", "structured"],
        default="summary",
        help="What to print to stdout",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return asyncio.run(_run(args))
    except KeyboardInterrupt:
        print("Interrupted")
        return 130


if __name__ == "__main__":
    sys.exit(main())
