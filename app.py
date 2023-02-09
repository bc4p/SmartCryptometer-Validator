# save this as app.py
from json import JSONDecodeError

from flask import Flask, render_template

app = Flask(__name__)
from mqtt_connection import create_mqtt_loop
import json

@app.route("/")
def hello():
    try:
        with open('data.json', 'r') as f:
            devices = json.load(f)
    except JSONDecodeError:
        print('error reading json')
    return render_template('./index.html', devices=sorted(devices.items()))


if __name__ == '__main__':
    client = create_mqtt_loop()
    # gunicorn.conf.py
    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()