# import paho.mqtt.client as mqtt #import the client1
# broker_address="127.0.0.1" 
# #broker_address="iot.eclipse.org" #use external broker
# client = mqtt.Client("P1") #create new instance
# client.connect(broker_address) #connect to broker
# client.publish("house/main-light","OFF")#publish


#simulator device 1 for mqtt message publishing
import paho.mqtt.client as paho
import time
import random
#hostname
import json
broker="localhost"
#port
port=1883
# def on_publish(client,userdata,result):
#     client.publish("/data",json.dumps(message))
#     pass

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