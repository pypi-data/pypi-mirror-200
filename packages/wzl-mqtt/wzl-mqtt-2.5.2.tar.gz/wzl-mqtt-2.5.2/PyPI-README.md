# WZL-MQTT

Current stable version: 2.5.2

## Documentation

For the full API documentation, view [https://iot.wzl-mq.rwth-aachen.de/documentation/libs/mqtt/](https://iot.wzl-mq.rwth-aachen.de/documentation/libs/mqtt/).

## Installation
Requires at least Python 3.6

1. Install the WZL-MQTT package via pip  
```
pip install wzl-mqtt
```

## Usage

### Publish messages

```python
from wzl import mqtt

# username and password required to connect to the broker
MQTT_USER = ""
MQTT_PASSWORD = ""

# address, port and virtual host of the broker to connect to 
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_VHOST = "/"

# initialize publisher and connect to the broker
client = mqtt.MQTTPublisher()
client.connect(MQTT_BROKER, MQTT_USER, MQTT_PASSWORD, vhost=MQTT_VHOST, port=MQTT_PORT)

# create message and publish the message as UTF-8 encoded string
message = json.dumps({"value": [random.uniform(0, 5) for i in range(3)], "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                                  "covariance": [[2, 0, 0], [0, 2, 0], [0, 0, 0]], "nonce": str(uuid.uuid4()), "hash": None, "unit": "MTR"})
client.publish(MQTT_USER + "/channel-001", message.encode("utf-8"))
```

### Subscribe to topics and receive messages
```python
from wzl import mqtt

# username and password required to connect to the broker
MQTT_USER = ""
MQTT_PASSWORD = ""

# address, port and virtual host of the broker to connect to 
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_VHOST = "/"

# initialize logger
logger = mqtt.Logger.get('Receiver') # change 'Receiver' to any string you like

# define callback which will be executed when a message is received
def print_mqtt_message(topic, message):
        logger.info("### {} ###\r\n{}\r\n".format(topic, message.decode("utf-8")))

# initialize subscriber and connect to the broker   
client = mqtt.MQTTSubscriber()
client.connect(MQTT_BROKER, MQTT_USER, MQTT_PASSWORD, vhost=MQTT_VHOST, port=MQTT_PORT)

# register the callback and subscribe topic
client.set_callback("PRINT", print_mqtt_message)
client.subscribe('#')

# start waiting loop to prevent program from exiting
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

```

## Changelog

**2.5.2** - 2023-03-29
  - client handles slash in at the end of prefix and the beginning of topic to avoid multiple consecutive slashes correctly now

2.5.1
  - increased verbosity in case of errors by including the full stack trace

2.5.0
  - changed signature of connect method
    - specifying the port is optional now, if not specified the port automatically is derived from the "websocket" and "ssl" flags
    
2.4.2
  - fixed a bug of websocket connection

2.4.1
- made the error message of code 1 more precise

2.4.0
- added vhost parameter to connect function of client
- changed default logging behaviour
  - now by default logging is only written to console
  - if logging should also create log-files, the logger must be explicitly initialized

2.3.0
- a prefix can now be defined which is prepended to every published or subscribed topic

2.2.0
- it is possible to connect with more than one client with an identical username to the broker

2.1.0
- removed wzl-utilities dependency

2.0.0
- renamed the MQTReceiver to MQTTSubscriber for the sake of convenience
- added extensive documentation

1.3.0
- added wzl-utilities dependency by sourcing out logging functionality
