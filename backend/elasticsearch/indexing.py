# app/elasticsearch/indexing.py

from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def index_user_recommendations(user_id: int, song_ids: list[int]):
    es.index(
        index="recommendations",
        id=user_id,
        body={
            "user_id": user_id,
            "recommended_songs": song_ids
        }
    )
