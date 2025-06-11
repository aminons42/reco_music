from kafka import KafkaConsumer
import json
from backend.tasks.recommendations import compute_recommendations

# Configure le consumer Kafka
consumer = KafkaConsumer(
    'musicdb.interactions',  # nom du topic créé par Debezium
    bootstrap_servers=['kafka:9092'],  # nom du service kafka dans docker-compose
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='reco-group'
)

print("Kafka consumer started, waiting for messages...")

for message in consumer:
    data = message.value
    print(f"Received interaction: {data}")
    user_id = data.get('user_id')
    if user_id:
        # Déclenche la tâche Celery pour recalculer les recommandations
        compute_recommendations.delay(user_id)
        print(f"Triggered recommendation task for user {user_id}")