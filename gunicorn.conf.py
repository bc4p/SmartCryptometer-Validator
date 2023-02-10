from mqtt_connection import create_mqtt_loop

client = None
def on_starting(server):
    global client
    client = create_mqtt_loop()

def on_exit(server):
    global client
    if client:
        client.disconnect()
        client.loop_stop()