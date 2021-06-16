import random
import tkinter as tk
from paho.mqtt import client as mqtt_client
import time

# broker = 'broker.emqx.io'
broker='localhost'
port = 1883
topic = 'python/mqtt_zxl'
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


def subscribe(client: mqtt_client):
    def on_massage(client, userdata, msg):
        print(f"Receved'{msg.payload.decode()}'from'{msg.topic}'topic")

    client.subscribe(topic)
    client.on_massage = on_massage

def publish(client):
    msg_count=0
    while True:
        time.sleep(1)
        msg=f"message:{msg_count}"
        result=client.publish(topic,msg)
        status=result[0]
        if status==0:
            print(f"Send'{msg}'to topic '{topic}'")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count+=1

def run():
    client = connect_mqtt()

    publish(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
