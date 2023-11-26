import paho.mqtt.client as mqtt
import redis
import json
r = redis.Redis()

broker="localhost"
port=1883

#time to live
timelive=60
def on_connect(client, userdata, flags, rc):
    print("Connected!")
    client.subscribe("/data")

def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode())
    print(message)
    r.set("speed", message.get("speed"))
    
client = mqtt.Client()
client.connect(broker,port,timelive)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()