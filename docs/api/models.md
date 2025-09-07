# Models API Reference

::: crawlstudio.models.CrawlConfig
    options:
      show_source: true
      docstring_style: google
      members:
        - firecrawl_api_key
        - google_api_key
        - crawl4ai_api_key
        - timeout
        - user_agent

::: crawlstudio.models.CrawlResult
    options:
      show_source: true
      docstring_style: google
      members:
        - url
        - backend_used
        - markdown
        - raw_html
        - structured_data
        - metadata
        - execution_time
        - cache_hit