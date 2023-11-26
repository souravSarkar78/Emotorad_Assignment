
import paho.mqtt.client as paho
import time
import random
import json


broker="localhost"
port=1883

client= paho.Client("admin")
client.connect(broker,port)


while True:
    inp = input("Input data: ")
    try:
        inp = json.loads(inp)
        speed = inp.get('speed')
        if speed:
            if speed<0 or speed>100:
                print("speed limit 0-100")
                continue
            ret= client.publish("/data",json.dumps({"speed": speed}))
        else:
            print("Invalid input")
    except:
        print("Invalid Input")