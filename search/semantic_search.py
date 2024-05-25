from elasticsearch import Elasticsearch, helpers
from pythonProject.DataQueryResponder.database import database_manager


es_host = 'localhost'
es_port = 9200
index_name = 'knowledge_base'

db_manager = database_manager.DBManager()
es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={
        "settings": {
            "analysis": {
                "analyzer": {
                    "russian_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "russian_stop", "russian_stemmer"]
                    }
                },
                "filter": {
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "articles": {
                    "type": "text",
                    "analyzer": "russian_analyzer"
                }
            }
        }
    })


def create_actions(rows, index_name):
    actions = [
        {
            "_index": index_name,
            "_id": row[0],
            "_source": {
                "articles": row[1],
                "subsubcategory": row[2],
                "subcategory": row[3],
                "category": row[4]
            }
        }
        for row in rows
    ]
    return actions


for rows in db_manager.fetch_data():
    actions = create_actions(rows, index_name)
    helpers.bulk(es, actions)

db_manager.close_connection()

def search_articles(query, index_name):
    search_query = {
        "query": {
            "match": {
                "articles": query
            }
        }
    }

    response = es.search(index=index_name, body=search_query)
    return response


def process_search_results(response):
    hits = response.get('hits', {}).get('hits', [])
    if not hits:
        return "No articles found."

    results = []
    for hit in hits:
        source = hit['_source']
        result = {
            "articles": source.get('articles', ''),
            "subsubcategory": source.get('subsubcategory', ''),
            "subcategory": source.get('subcategory', ''),
            "category": source.get('category', '')
        }
        results.append(result)

    return results


query = "технологий"
response = search_articles(query, index_name)
print(response)
results = process_search_results(response)

for result in results:
    print(f"Article: {result['articles']}")
    print(f"Subsubcategory: {result['subsubcategory']}")
    print(f"Subcategory: {result['subcategory']}")
    print(f"Category: {result['category']}")
    print("-" * 40)
