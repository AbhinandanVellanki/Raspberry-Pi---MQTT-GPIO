import RPi.GPIO as GPIO
import time
import threading
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

hostname = "iot.eclipse.org"  # Sandbox broker
port = 1883  # Default port for unencrypted MQTT

topic_state = "PC000/traffic_light/state"  # '/' is used as the delimiter for sub-topics

def on_connect(client, userdata, flags, rc):
    # Successful connection is '0'
    print("[MQTT] Connection result: " + str(rc))

def on_publish(client, userdata, mid):
    print("[MQTT] Sent: " + str(mid))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("[MQTT] Disconnected unexpectedly")

# Initialize server instance
mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_disconnect = on_disconnect
mqttc.connect(hostname, port=port,keepalive=60, bind_address="")
mqttc.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
red_led=4
green_led=8
wait_button=14
wait_led=7
redon=False
GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(green_led,GPIO.OUT)
red_start_time=0

def on_light(light, delay):
    GPIO.output(light,1)
    time.sleep(delay)
    GPIO.output(light,0)

def blink_light(light,delay):
    ctr=0
    while ctr<=delay:
        GPIO.output(light,0)
        time.sleep(1)
        ctr+=1
        if ctr==delay:
            break
        GPIO.output(light,1)
        time.sleep(1)
        ctr+=1
    GPIO.output(light,0)

class waitThread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
        
    def run(self):
        global red_led
        global wait_button
        global wait_led
        global redon
        global red_start_time
        while redon==False:
            time.sleep(0)
        if redon==True:
            GPIO.setup(wait_button, GPIO.IN, GPIO.PUD_UP)
            GPIO.setup(wait_led,GPIO.OUT)
        while True:
            if(GPIO.input(wait_button))==False :
                start_time=time.time()
                while(GPIO.input(wait_button))==False:
                    if (time.time()-start_time) >= 0.5:
                        GPIO.output(wait_led,1)
                end_time=time.time()
                interval=end_time-red_start_time
                if interval<5:
                      time.sleep(5-interval)
                      time.sleep(3)
                      GPIO.output(red_led,0)
                      GPIO.output(wait_led,0)
                      redon=False
                elif interval >=5:
                      time.sleep(3)
                      GPIO.output(red_led,0)
                      GPIO.output(wait_led,0)
                      redon=False
        
try:
    thread1=waitThread(1,"Thread-1")
    thread1.daemon=True
    thread1.start()
    GPIO.output(red_led,0)
    while True:
        mqttc.publish(topic_state, 1, qos=0, retain=False)  # State 1
        on_light(green_led,5)
        mqttc.publish(topic_state, 2, qos=0, retain=False)  # State 2
        blink_light(green_led,3)
        GPIO.output(red_led,1)
        red_start_time=time.time()
        redon=True
        mqttc.publish(topic_state, 3, qos=0, retain=False)  # State 3
        while redon==True:
            time.sleep(0)
except KeyboardInterrupt:
    print("CTRL-C: Terminating program")
finally:
    print(" Cleaning up GPIO")
    GPIO.cleanup()
