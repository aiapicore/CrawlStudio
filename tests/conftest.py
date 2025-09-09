"""
Pytest configuration file for CrawlStudio tests
"""
import pytest


def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line(
        "markers",
        "essential: mark test as essential for CI pipeline"
    )
