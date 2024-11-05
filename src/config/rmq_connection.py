import os
import pika
from dotenv import load_dotenv

load_dotenv()

def rmq_connection() -> pika.BlockingConnection:
  user = os.getenv("RMQ_USER")
  password = os.getenv("RMQ_PASS")
  host = os.getenv("RMQ_HOST")
  port = int(os.getenv("RMQ_PORT"))
  vhost = os.getenv("RMQ_VHOST")

  try:
    credentials = pika.PlainCredentials(username=user, password=password)

    parameters = pika.ConnectionParameters(
      host=host,
      port=port,
      virtual_host=vhost,
      credentials=credentials,
      heartbeat=60
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    print("RabbitMQ connected successfully")
    return channel
  except Exception as e:
    print("Failed to create RabbitMQ connection:", e)
    raise
