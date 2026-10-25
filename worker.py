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

orders = [
    {
        "event_id": str(uuid.uuid4()),
        "order_id": "order-101",
        "item_id": "laptop",
        "quantity": 1
    },
    {
        "event_id": str(uuid.uuid4()),
        "order_id": "order-102",
        "item_id": "keyboard",
        "quantity": 2
    },
    {
        "event_id": str(uuid.uuid4()),
        "order_id": "order-103",
        "item_id": "mouse",
        "quantity": 1
    },
    {
        "event_id": str(uuid.uuid4()),
        "order_id": "order-104",
        "item_id": "monitor",
        "quantity": 2
    }
]

for order in orders:
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(order),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    print(
        f"[Producer] Published "
        f"order_id={order['order_id']} "
        f"item_id={order['item_id']} "
        f"quantity={order['quantity']} "
        f"event_id={order['event_id']}"
    )

connection.close()

print("[Producer] Finished publishing orders.")