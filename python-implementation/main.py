import machine
import time
import sender
from machine import Pin

rtc = machine.RTC()

led = machine.Pin(5, machine.Pin.OUT)
def main():
  while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
    sender.send(b'id: 1, timestamp: 102')
    print(ds.datetime())

main()


