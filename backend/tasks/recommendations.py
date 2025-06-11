# celery_tasks/recommendation.py
import numpy as np
import pandas as pd
from backend.celery_worker import celery_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.db.models import Interaction, Song
from sklearn.metrics.pairwise import cosine_similarity
from backend.elasticsearch.indexing import index_recommendations

DATABASE_URL = "mysql+pymysql://root:root@mysql:3306/musicdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task
def compute_recommendations(user_id: int):
    session = SessionLocal()
    try:
        # 1. Récupère toutes les interactions
        interactions = session.query(Interaction).all()
        if not interactions:
            print("Aucune interaction trouvée.")
            return

        # 2. Crée la matrice utilisateur-chanson
        data = [(i.user_id, i.song_id, 1 if i.liked else 0) for i in interactions]
        df = pd.DataFrame(data, columns=['user_id', 'song_id', 'liked'])
        matrix = df.pivot_table(index='user_id', columns='song_id', values='liked').fillna(0)

        # 3. Calcule la similarité cosinus entre utilisateurs
        similarity = cosine_similarity(matrix)
        sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

        # 4. Trouve les utilisateurs similaires
        if user_id not in sim_df.index:
            print(f"user_id {user_id} non trouvé dans la matrice.")
            return

        similar_users = sim_df[user_id].sort_values(ascending=False)[1:6]  # top 5 similaires

        # 5. Récupère les chansons likées par les utilisateurs similaires mais pas par l'utilisateur courant
        user_songs = set(df[df['user_id'] == user_id]['song_id'])
        similar_users_ids = similar_users.index.tolist()
        candidate_songs = df[(df['user_id'].isin(similar_users_ids)) & (df['liked'] == 1)]['song_id']
        recommended_songs = set(candidate_songs) - user_songs

        # 6. Affiche ou sauvegarde les recommandations
        print(f"Recommandations pour user {user_id}: {list(recommended_songs)}")
        # Indexe dans Elasticsearch
        index_recommendations(user_id, recommended_songs)
        return list(recommended_songs)
    except Exception as e:
        print(f"Erreur lors du calcul des recommandations: {e}")
    finally:
        session.close()
