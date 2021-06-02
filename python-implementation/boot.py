# Complete project details at https://RandomNerdTutorials.com

import time

import esp
import machine
import network
import ubinascii
from umqttsimple import MQTTClient

esp.osdebug(None)
import gc
gc.collect()

ssid = 'Max'
password = 'havanagila'
mqtt_server = 'broker.hivemq.com'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'secterica/goon-gateways/race_info'
topic_pub = b'secterica/goon-gateways/race_info'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'secterica/goon-gateways/race_info' and msg == b'hello':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

client = None

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

    
def send(msg):
  try:
    client.check_msg()
    client.publish(topic_pub, msg)
  except OSError as e:
    restart_and_reconnect()


