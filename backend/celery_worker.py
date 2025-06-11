from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",  # Change selon ton broker (ex: RabbitMQ)
    backend="redis://localhost:6379/0"
)