from grove.grove_button import GroveButton
from grove.grove_led import GroveLed
from datetime import datetime as dt, timedelta
import time
from morseDict import MORSE_CODE_DICT
from grove.factory import Factory
# connect to pin 5 (slot D5)
PIN = 5
button = GroveButton(PIN)
led = GroveLed(16)

press = dt.now()
release = dt.now()

baseSecTimer = input("Please select the timing beat")
print("Timing base selected, now its {} secs".format(baseSecTimer))

while True:
	button.on_press = press
	button.on_release = release

	elapse = timedelta(press-release)
	if elapse.total_seconds() > 5 :
		print("asdas")
		startEngine()


def startEngine():
	print("Starting Morse Detector")
	time.sleep(2)
	print("Please press button to start submit your 4-digit pin")
 
	pinNumber = get_Ping_Code()
	print(pinNumber)

def get_Ping_Code(pinCode = []):
	while len(pinCode) < 4:
		print("Leyendo la posicion {} del pin de 4 digitos".format(len(pinCode)))
  
		#Itera hasta tener una string de 5 digitos 
		codeString = pin_String()
		#string valida, sino volvemos a iterar
		if codeString in MORSE_CODE_DICT.values():
			pinConvertido = MORSE_CODE_DICT.keys()[MORSE_CODE_DICT.values().index(codeString)]
			pinCode.append(pinConvertido)
		else:
			print("Pin no valido, repetir digitos!")
		get_Ping_Code(pinCode)
	return pinCode
        
def pin_String(codeString = ""):
    
	while len(codeString) < 5:
		button.on_press = press
		button.on_release = release

		elapse = timedelta(press-release)
		if elapse.total_seconds() (2/baseSecTimer):
			codeString += '-'
			print("Tu string: {},  ahora lleva una - mas".format(codeString))
			pin_String(codeString)
		elif elapse.total_seconds() < (1/baseSecTimer):
			codeString += '.'
			print("Tu string: {},  ahora lleva una . mas".format(codeString))
			pin_String(codeString)
		else:
			print("NOse que pusiste")
			pin_String(codeString)
	return codeString 



