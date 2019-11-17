from grove.grove_button import GroveButton
from grove.grove_led import GroveLed
import time
from grove.factory import Factory


# connect to pin 5 (slot D5)
PIN = 5
button = GroveButton(PIN)
led = GroveLed(16)
lcd = Factory.getDisplay("JHD1802")
rows, cols = lcd.size()
print("LCD model: {}".format(lcd.name))
print("LCD type : {} x {}".format(cols, rows))

lcd.setCursor(0, 0)
lcd.write("hello world!")
lcd.setCursor(0, cols - 1)
lcd.write('X')
lcd.setCursor(rows - 1, 0)

for i in range(cols):
  lcd.write(chr(ord('A') + i))
  
time.sleep(3)
lcd.clear()
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