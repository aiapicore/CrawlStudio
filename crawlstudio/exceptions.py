class CrawlError(Exception):
    """Base exception for CrawlStudio errors."""


class ConfigurationError(CrawlError):
    """Raised when configuration or environment variables are invalid/missing."""


class DependencyMissingError(CrawlError):
    """Raised when an optional/required dependency is not installed."""


class BackendExecutionError(CrawlError):
    """Raised when a backend fails during execution."""
