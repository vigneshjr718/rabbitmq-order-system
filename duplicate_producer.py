import json
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
    "event_id": "duplicate-test-001",
    "order_id": "duplicate-order-001",
    "item_id": "headphones",
    "quantity": 1
}

for attempt in range(1, 3):
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(order),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    print(
        f"[Duplicate Producer] Published "
        f"attempt={attempt} "
        f"event_id={order['event_id']}"
    )

connection.close()

print(
    "[Duplicate Producer] "
    "Same event_id published twice."
)