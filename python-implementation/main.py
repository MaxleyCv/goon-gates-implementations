import machine
import time
import boot
from machine import Pin
import clustering

rtc = machine.RTC()

ECHO = 34
TRIGGER = 35

trigger_pin = machine.Pin(TRIGGER, machine.Pin.OUT)
echo_pin = machine.Pin(ECHO, machine.Pin.IN)

previous = 0
last_ten = [100 for _ in range(10)]
last_two_thousand = [100 for _ in range(2000)]

def update_vals(newval, last_ten, last_two_thousand):
  last_ten = [last_ten[i + 1] for i in range(9)].append(newval)
  last_two_thousand = [last_two_thousand[i + 1] for i in range(1999)].append((sum(last_ten))/10)
  return last_ten, last_two_thousand

def find_data():
  global last_ten
  global last_two_thousand
  trigger_pin.value(1)
  time.sleep(0.0001)
  trigger_pin.value(0)
  val_cm = echo_pin.pulse_in() / 58
  last_ten, last_two_thousand = update_vals(val_cm, last_ten, last_two_thousand)


def main():
  while True:

    if time.time() - previous >= 1000:
      previous = rtc.datetime[8]
      if clustering.check(last_two_thousand):
        boot.send(bytes("id: 1, timestamp: {0}}".format(time.time())))
    find_data()


main()


