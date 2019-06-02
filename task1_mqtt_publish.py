import paho.mqtt.publish as publish

hostname = "iot.eclipse.org"  # Sandbox broker
port = 1883  # Default port for unencrypted MQTT

topic = "PC000/Abhi"  # '/' is used as the delimiter for sub-topics

publish.single(topic, payload="Hello, Abhi!", qos=0,
	hostname=hostname,
	port=port)
