from mqtt_connection import create_mqtt_loop

def on_starting(server):
    client = create_mqtt_loop()