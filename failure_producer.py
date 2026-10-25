import json
import uuid
import pika

QUEUE_NAME = "orders"

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue=QUEUE_NAME,
    durable=True
)

order = {
    "event_id": str(uuid.uuid4()),
    "order_id": "failure-test-001",
    "item_id": "laptop",
    "quantity": 1
}

channel.basic_publish(
    exchange="",
    routing_key=QUEUE_NAME,
    body=json.dumps(order),
    properties=pika.BasicProperties(
        delivery_mode=2
    )
)

print(
    "[Failure Producer] Published message:"
)

print(
    f"event_id={order['event_id']}"
)

print(
    f"order_id={order['order_id']}"
)

connection.close()