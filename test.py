from grove.grove_button import GroveButton
from grove.grove_led import GroveLed
from datetime import datetime as dt
import time
from morseDict import MORSE_CODE_DICT
from grove.factory import Factory
# connect to pin 5 (slot D5)
PIN = 5
button = GroveButton(PIN)
led = GroveLed(16)

#setting variables for out login process
baseSecTimer = input("Please select the timing beat in secs: ")
Tolerance =  baseSecTimer / 2.0
print("Timing base selected, now its {} secs".format(baseSecTimer))

pinCode= []
codeString = ''
onProcess = False

def startEngine():
	print("Starting Morse Detector")
	time.sleep(2)
	print("Please press button to start submit your 4-digit pin")

def get_Ping_Code(t):
	global codeString
	while len(pinCode) < 4:
		print("Leyendo la posicion {} del pin de 4 digitos".format(len(pinCode)))

		pin_String(t)
		if len(codeString) == 5:
			#string valida, sino volvemos a iterar
			if codeString in MORSE_CODE_DICT.values():
				pinConvertido = MORSE_CODE_DICT.keys()[MORSE_CODE_DICT.values().index(codeString)]
				pinCode.append(pinConvertido)
				codeString = ''
			else:
				print("Pin no valido, repetir digitos!")
				codeString = ''
		return True
	return pinCode

def pin_String(t):
	global codeString
	while len(codeString) < 5:
		
		if t > (2/baseSecTimer):
			codeString += '-'
			print("Tu string: {},  ahora lleva una - mas".format(codeString))
		elif t < (1/baseSecTimer):
			codeString += '.'
			print("Tu string: {},  ahora lleva una . mas".format(codeString))
		else:
			print("Nose que pusiste")
	return codeString 

def blink():
	while True:
		led.on()
		time.sleep(baseSecTimer / 2.0)
		led.off()
		time.sleep(baseSecTimer)
  
def on_Press(t):
    	"""
	funcion para imprimir current status
	"""
	print("SI funciona el boton, imprimire t:", t)

def on_Release(t):
	global onProcess
	"""
	funcion como controlador, iniciaria nuestras funciones 
	y hara algo con el valor obtenido del time
	"""
	print("Liberado: ", round(t,2))
	if not onProcess and t > 6:
		startEngine()
		blink()
		get_Ping_Code(t)
	elif onProcess and len(pinCode) == 4 and t > 6:
		print("Apagando!")
	elif onProcess:
		get_Ping_Code(t)
	else:
		print("NO entre!")

button.on_press = on_Press
button.on_release = on_Release
#start script
while True:
    time.sleep(1)
