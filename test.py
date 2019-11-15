from grove.grove_button import GroveButton
from grove.grove_led import GroveLed
import time
# connect to pin 5 (slot D5)
PIN = 5
button = GroveButton(PIN)
led = GroveLed(16)

def on_press(t):
  print('Button is pressed')
  led.on()
def on_release(t):
  print("Button is released, pressed for {0} seconds".format(round(t,6)))
  led.off()
button.on_press = on_press
button.on_release = on_release
while True:
  time.sleep(1)