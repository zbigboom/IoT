import random
import time
import pandas as pd

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt_dhu0"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def read_sensor():
    df_temperature = pd.read_csv('soi_data.csv')

    return df_temperature
    

def publish(client):
    dataset_t = read_sensor()
    dataset_length = len(dataset_t)
    msg_count = 1
    while True:
        time.sleep(1)
        msg_date = dataset_t.index[msg_count]
        msg_temperature = dataset_t.iloc[msg_count,0]
        msg = f"时间:{msg_date} 温度:{msg_temperature}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

        if msg_count < dataset_length - 1:
            msg_count += 1
        else:
            msg_count = 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
