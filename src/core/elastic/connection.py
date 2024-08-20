from elasticsearch import Elasticsearch

Elastic = Elasticsearch(
    hosts=[{"host": "elastic", "port": 9200, "scheme": "https"}],
    timeout=30,
    max_retries=10,
    retry_on_timeout=True,
)
