import paho.mqtt.client as mqtt

hostname = "iot.eclipse.org"  # Sandbox broker
port = 1883  # Default port for unencrypted MQTT

topic_state= "PC000/traffic_light/state"  # Wildcard character '#' indicates all sub-topics (e.g. PC000/test, PC000/sensor/temperature, etc.)
topic_emergency= "PC000/traffic_light/emergency"

def on_connect(client, userdata, flags, rc):
	# Successful connection is '0'
	print("Connection result: " + str(rc))
	if rc == 0:
		# Subscribe to topics
		client.subscribe(topic_state)
		client.subscribe(topic_emergency)
		
def on_message(client, userdata, message):
        if message.topic == "PC000/traffic_light/state":
                print("Received message on %s: %s (QoS = %s)" % 
		(message.topic, message.payload.decode("utf-8"), str(message.qos)))
        elif message.topic == "PC000/traffic_light/emergency":
                print("Received message on %s: Emergency Status: %s (QoS = %s)" % 
		(message.topic, message.payload.decode("utf-8"), str(message.qos)))

                
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print("Disconnected unexpectedly")

# Initialize client instance
client = mqtt.Client()

# Bind events to functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the specified broker
client.connect(hostname, port=port)

# Network loop runs in the background to listen to the events
client.loop_forever()
