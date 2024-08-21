from elasticsearch import AsyncElasticsearch

Elastic = AsyncElasticsearch(
    hosts=[{"host": "elastic", "port": 9200, "scheme": "http"}],
    max_retries=5,
    retry_on_timeout=True,
)
