import json
import os
import time
import pika

QUEUE_NAME = "orders"
PROCESSED_FILE = "processed_events.txt"

worker_name = os.environ.get("WORKER_NAME", "Worker")


def load_processed_events():
    if not os.path.exists(PROCESSED_FILE):
        return set()

    with open(PROCESSED_FILE, "r") as file:
        return {
            line.strip()
            for line in file
            if line.strip()
        }


def save_event(event_id):
    with open(PROCESSED_FILE, "a") as file:
        file.write(event_id + "\n")


def callback(ch, method, properties, body):
    order = json.loads(body)

    event_id = order["event_id"]

    print(
        f"\n[{worker_name}] Received "
        f"order_id={order['order_id']} "
        f"item_id={order['item_id']} "
        f"quantity={order['quantity']} "
        f"event_id={event_id}"
    )

    # Reload the file for each message so both worker
    # processes see the latest processed event IDs.
    processed_events = load_processed_events()

    if event_id in processed_events:
        print(
            f"[{worker_name}] DUPLICATE detected: "
            f"event_id={event_id}"
        )

        print(
            f"[{worker_name}] Business action skipped."
        )

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

        print(
            f"[{worker_name}] Duplicate acknowledged."
        )

        return

    print(f"[{worker_name}] Processing order...")

    # Simulate business processing
    time.sleep(5)

    save_event(event_id)

    print(f"[{worker_name}] Processing complete.")

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )

    print(f"[{worker_name}] ACK sent.")


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue=QUEUE_NAME,
    durable=True
)

# Give each worker one unacknowledged message at a time.
channel.basic_qos(
    prefetch_count=1
)

channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
    auto_ack=False
)

print(
    f"[{worker_name}] Waiting for orders. "
    f"Press CTRL+C to stop."
)

try:
    channel.start_consuming()

except KeyboardInterrupt:
    print(f"\n[{worker_name}] Worker stopped.")

finally:
    if connection.is_open:
        connection.close()