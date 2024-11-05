import pika
from src.config.rmq_connection import rmq_connection
from src.service.rmq_service import consume_messages

if __name__ == "__main__":
  channel: pika.BlockingConnection = rmq_connection()
  consume_messages(channel)