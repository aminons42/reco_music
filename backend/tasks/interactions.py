# app/tasks/interaction_tasks.py
from app.celery_worker import celery_app

@celery_app.task
def process_user_interaction(data):
    print("Processing interaction:", data)
    # Example logic (in real case, you save or analyze the interaction)
@celery_app.task
def generate_recommendations(user_id: int):
    print(f"Generating recommendations for user {user_id}")
    # TODO: Add recommendation logic here
