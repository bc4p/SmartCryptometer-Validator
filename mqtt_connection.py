from json import JSONDecodeError

from nacl.signing import VerifyKey
import ed25519
import paho.mqtt.client as mqttClient
import time
import json
from threading import Lock
import os
import logging


log = logging.getLogger('validator')
log.setLevel(logging.INFO)

lock = Lock()
with open('pub_keys.json') as f:
    pub_keys = json.load(f)

Connected = False  # global variable for the state of the connection

broker_address = os.getenv('MQTT_BROKER', "bc4p.nowum.fh-aachen.de")
port = os.getenv('MQTT_PORT', 1883)  # Broker port
user = os.getenv('MQTT_USER', "bc4p")  # Connection username
password = os.getenv('MQTT_PASSWORD', "9ykCLBW3usTuZnoZieAt")  # Connection password


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        log.info("Connection failed")

def on_message(client, userdata, message):
    json_data = json.loads(message.payload)
    if json_data.get('Signature'):
        topic = message.topic
        start = topic.index('/')
        end = topic.index('/', start + 1)

        subtopic = topic[start + 1:end]
        log.info(f"The public key is: {pub_keys.get(subtopic)}")
        log.info(f"Full Topic:{message.topic}")
        log.info(f'Message Payload: {json.loads(message.payload)}')
        key = ed25519.from_ascii(pub_keys.get(subtopic), encoding='hex')
        signature = ed25519.from_ascii(json_data.get('Signature'), encoding='hex')
        verify_key = VerifyKey(key)
        log.info(f'{json_data.get("Time")},{json_data.get("ENERGY").get("Total")}')
        try:
            verify_key.verify(smessage=f'{json_data.get("Time")},{json_data.get("ENERGY").get("Total")}'.encode(),
                             signature=signature)
            verified_bool = True
            log.info('MESSAGE VERIFIED!')
        except Exception:
            verified_bool = False
            log.info(f'broken signature for {subtopic}')
        # save to json
        meter_value = {
            'total': json_data.get("ENERGY").get("Total"),
            'time': json_data.get("Time"),
            'verified': verified_bool
        }

        with lock:
            try:
                with open('data.json', 'r') as f:
                    last_signed_values = json.load(f)
            except Exception:
                last_signed_values = {}
                log.info('Error reading json')

            last_signed_values[subtopic] = meter_value
            with open('data.json', 'w') as f:
                json.dump(last_signed_values, f)


def create_mqtt_loop():
    client = mqttClient.Client("Tasmota Meter Verifier2")
    client.username_pw_set(user, password=password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)  # connect to broker
    client.loop_start()  # start the loop

    while not Connected:
        time.sleep(0.1)

    client.subscribe("tele/+/SENSOR")
    return client


if __name__ == '__main__':
    client = create_mqtt_loop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("exiting")
        client.disconnect()
        client.loop_stop()
