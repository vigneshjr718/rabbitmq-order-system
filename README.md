RabbitMQ Order Processing System

Overview

This project demonstrates asynchronous message processing using RabbitMQ and Python. An Order Producer publishes order events to a RabbitMQ queue, while independent Order Worker processes consume and process those events.

The project demonstrates manual acknowledgments, competing consumers, message redelivery after a worker failure, and duplicate-event handling.

Architecture

flowchart LR
    P[Order Producer] -->|Publish Order Event| Q[(RabbitMQ orders Queue)]
    Q --> W1[Order Worker 1]
    Q --> W2[Order Worker 2]
    W1 -->|ACK after processing| Q
    W2 -->|ACK after processing| Q

Components

Order Producer

producer.py publishes multiple order messages to the RabbitMQ orders queue.

Each message contains:

* event_id
* order_id
* item_id
* quantity

Order Workers

worker.py consumes messages from the orders queue.

Each worker:

* Receives order messages
* Logs the order being processed
* Processes the message
* Sends an ACK only after processing finishes
* Tracks processed event_id values
* Detects duplicate events and skips duplicate business actions

Two worker processes can run simultaneously as competing consumers.

RabbitMQ

RabbitMQ provides the orders queue and delivers each message to an available worker.

Requirements

* Python 3
* Docker Desktop
* RabbitMQ
* pika

Install the Python dependency with:

pip install -r requirements.txt

Running RabbitMQ

RabbitMQ is run using Docker:

docker run -d --name rabbitmq-lab -p 5672:5672 -p 15672:15672 rabbitmq:3-management

If the container already exists but is stopped:

docker start rabbitmq-lab

RabbitMQ Management UI:

http://localhost:15672

Default credentials:

Username: guest
Password: guest

Running Worker 1

PowerShell:

$env:WORKER_NAME="Worker-1"
python worker.py

Running Worker 2

Open another PowerShell terminal:

$env:WORKER_NAME="Worker-2"
python worker.py

Both workers consume messages from the same orders queue.

Running the Producer

Open another terminal:

python producer.py

The producer publishes multiple order events to RabbitMQ.

Competing Consumers

When Worker 1 and Worker 2 are running simultaneously, RabbitMQ distributes messages between them.

Each individual message is handled by only one worker.

Evidence will be added after execution.

Failure and Redelivery

failure_producer.py publishes a single test message.

The failure test demonstrates what happens when a worker receives a message but terminates before sending its ACK.

Because the message was not acknowledged, RabbitMQ returns it to the queue and another worker can receive it.

Evidence will be added after execution.

Duplicate Handling

duplicate_producer.py publishes the same event_id twice.

Workers keep track of previously processed event IDs using processed_events.txt.

If the same event ID is received again, the worker logs:

DUPLICATE detected
Business action skipped.

The duplicate message is acknowledged without performing the business operation again.

Evidence will be added after execution.

Evidence

Execution screenshots will be added to the screenshots directory after testing.

Reflection

A RabbitMQ message can be delivered more than once when a consumer receives the message but fails before sending an acknowledgment. RabbitMQ cannot know whether the business operation completed, so an unacknowledged message may be delivered to another consumer. Idempotent handling prevents the same business action from being performed multiple times by tracking previously processed event IDs. This allows consumers to safely handle message redelivery and duplicate messages.