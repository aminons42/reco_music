from kafka import KafkaConsumer
import json
from celery_app.tasks.recommendations import generate_user_recommendations_task

KAFKA_TOPIC = "dbserver1.music_db.user_song_interactions"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

def start_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="recommendation-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    print(f"Listening to Kafka topic: {KAFKA_TOPIC}")
    for message in consumer:
        try:
            payload = message.value
            after = payload.get("payload", {}).get("after")

            if after:
                user_id = after.get("user_id")
                print(f"[Kafka] Triggering recommendation task for user_id={user_id}")
                generate_user_recommendations_task.delay(user_id)
        except Exception as e:
            print(f"[Kafka] Error processing message: {e}")
