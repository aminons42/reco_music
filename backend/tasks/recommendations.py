# celery_tasks/recommendation.py
import numpy as np
import pandas as pd
from celery import shared_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.models import Interaction, Recommendation, Song  # adjust import path

DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost:3306/yourdatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@shared_task
def compute_recommendations(user_id: int):
    session = SessionLocal()
    try:
        # 1. Get all user-song interactions (likes/dislikes)
        interactions = session.query(Interaction).all()
        if not interactions:
            return

        # 2. Create user-item matrix
        data = [(i.user_id, i.song_id, 1 if i.type == 'like' else -1) for i in interactions]
        df = pd.DataFrame(data, columns=['user_id', 'song_id', 'value'])
        matrix = df.pivot_table(index='user_id', columns='song_id', values='value').fillna(0)

        # 3. Compute cosine similarity for users
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(matrix)
        sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

        # 4. Get top similar users to target user
        if user_id not in sim_df.index:
            return

        similar_users = sim_df[user_id].sort_values(ascending=False)[1:6]  # top 5 similar users

        # 5. Get songs liked by similar users but not interacted by current user
        user_songs = set(df[df['user_id'] == user_id]['song_id'])
        similar_users_ids = similar_users.index.tolist()
        candidate_songs = df[(df['user_id'].isin(similar_users_ids)) & (df['value'] > 0)]['song_id']
        recommended = candidate_songs[~candidate_songs.isin(user_songs)].value_counts().head(10).index.tolist()

        # 6. Save to Recommendation table
        session.query(Recommendation).filter_by(user_id=user_id).delete()
        for song_id in recommended:
            session.add(Recommendation(user_id=user_id, song_id=song_id))
        session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
