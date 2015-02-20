## What this does

This watches for a change in pin 18, which is connected to a reed sensor on the bathroom stall door. When a change happens, a message with the current status of the door and a timestamp is sent to RabbitMQ.
