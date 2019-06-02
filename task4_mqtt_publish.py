import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time

hostname = "iot.eclipse.org"  # Sandbox broker
port = 1883  # Default port for unencrypted MQTT

topic_emergency = "PC000/traffic_light/emergency"  # '/' is used as the delimiter for sub-topics

def on_connect(client, userdata, flags, rc):
    # Successful connection is '0'
    print("[MQTT] Connection result: " + str(rc))

def on_publish(client, userdata, mid):
    time.sleep(0)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("[MQTT] Disconnected unexpectedly")

#initializing server instance
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_disconnect = on_disconnect
mqttc.connect(hostname, port=port,keepalive=60, bind_address="")
mqttc.loop_start()
    
mqttc.publish(topic_emergency, False, qos=0, retain=False)  # State 1
print("Sent Emergency state: False")

time.sleep(10)

mqttc.publish(topic_emergency, True, qos=0, retain=False)  # State 1
print("Sent Emergency state: True")
