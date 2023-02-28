# BC4P Smart Cryptometer Validator
This is Validator for signed values from Tasmota cryptometers which have been flashed with the [BC4P forked Tasmota Firmware](https://github.com/bc4p/Tasmota)

This validator Takes the last sent MQTT messages of the Tasmota devices and shows wheater their messages are verified through the use of Asymmetric Enryption.

## Setup
Make sure to edit the following file:

- `pub_keys.json` contains the public keys of the BC4P flashed Tasmota deivces. Be sure to save them in the format of `"DEVICE NAME":"PUBLIC KEY"`
- create a file `.env` which should contain the fields MQTT_HOST, MQTT_PORT, MQTT_USER and MQTT_PASSWORD

After cloning this repository you can run `sudo docker build -t tasmota-validator .` to build the docker image and `sudo docker run -ti tasmota-validator` to run the image
