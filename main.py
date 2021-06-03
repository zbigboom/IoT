import random
import tkinter as tk
from paho.mqtt import client as mqtt_client
import time

broker = 'broker.emqx.io'
port = 1883
topic = '/python/mqtt_zxl'
clinent_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect,return code %d\n', rc)

    client = mqtt_client.Client(clinent_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def disconnect_mqtt() -> mqtt_client:
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    client = mqtt_client.Client(clinent_id)
    client.on_disconnect = on_disconnect


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Receved'{msg.payload.decode()}'from'{msg.topic}'topic")

    client.subscribe(topic)
    client.on_message = on_message


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"message:{msg_count}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send'{msg}'to topic '{topic}'")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    subscribe(client)
    # publish(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
