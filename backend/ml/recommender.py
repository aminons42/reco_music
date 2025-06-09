# app/ml/recommender.py

from sqlalchemy.orm import Session
from app.db.models import UserSongInteraction, Song
from collections import Counter

def generate_recommendations(db: Session, user_id: int, top_n: int = 10):
    """
    Very simple recommendation:
    - Find users who listened to similar songs
    - Recommend what they liked that the current user hasn’t seen
    """

    # Get songs user has listened to
    user_songs = db.query(UserSongInteraction.song_id).filter(
        UserSongInteraction.user_id == user_id
    ).distinct()

    user_song_ids = [s.song_id for s in user_songs]

    # Find other users who listened to the same songs
    similar_users = db.query(UserSongInteraction.user_id).filter(
        UserSongInteraction.song_id.in_(user_song_ids),
        UserSongInteraction.user_id != user_id
    ).distinct()

    similar_user_ids = [u.user_id for u in similar_users]

    # Get what they listened to
    candidate_songs = db.query(UserSongInteraction.song_id).filter(
        UserSongInteraction.user_id.in_(similar_user_ids)
    ).all()

    # Count most popular ones
    song_counts = Counter([s.song_id for s in candidate_songs if s.song_id not in user_song_ids])
    recommended_song_ids = [song_id for song_id, _ in song_counts.most_common(top_n)]

    return recommended_song_ids
