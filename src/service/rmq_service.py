import os
import json
import pika
from dotenv import load_dotenv

from src.service.ftp_service import download_image, upload_image
from src.service.predict import predict_image
from src.service.database_service import save_to_database

load_dotenv()

def consume_messages(channel: pika.BlockingConnection) -> None:
  queue_name: str = os.getenv("RMQ_QUEU")

  def callback(ch, method, properties, body):
    message_str = body.decode('utf-8')
    
    message_dict = json.loads(message_str)
    print(f"Received message as dictionary: {message_dict}")

    image_filename: str = message_dict.get("value")

    download_image(image_filename)
    
    output_image: str = predict_image(image_filename)
    
    if output_image:
      upload_image(output_image)
      save_to_database(output_image)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

  channel.basic_consume(queue=queue_name, on_message_callback=callback)

  print(f"Waiting for messages in queue: {queue_name}. To exit press CTRL+C.")

  try:
    channel.start_consuming()
  except KeyboardInterrupt:
    print("Stopped consuming messages.")
    channel.close()
