# app/elasticsearch/indexing.py

from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")

def index_recommendations(user_id, song_ids):
    doc = {
        "user_id": user_id,
        "recommended_songs": list(song_ids)
    }
    es.index(index="recommendations", id=user_id, document=doc)

def get_recommendations(user_id):
    try:
        res = es.get(index="recommendations", id=user_id)
        return res["_source"]["recommended_songs"]
    except Exception:
        return []

def index_song(song):
    doc = {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "release_year": song.release_year
    }
    es.index(index="songs", id=song.id, document=doc)

def search_songs_es(query, skip=0, limit=10):
    res = es.search(
        index="songs",
        from_=skip,
        size=limit,
        query={
            "multi_match": {
                "query": query,
                "fields": ["title", "artist", "genre"]
            }
        }
    )
    return [hit["_source"] for hit in res["hits"]["hits"]]
