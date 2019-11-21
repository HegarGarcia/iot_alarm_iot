from grove.grove_button import GroveButton
from grove.grove_led import GroveLed
from datetime import datetime as dt
import time
from morseDict import MORSE_CODE_DICT
from grove.factory import Factory
import threading
# connect to pin 5 (slot D5)
PIN = 5
button = GroveButton(PIN)
led = GroveLed(16)

baseSecTimer = input("Please select the timing beat")
print("Timing base selected, now its {} secs".format(baseSecTimer))

def on_Press(t):
	"""
	funcion para imprimir current status
	"""
	print("SI funciona el boton, imprimire t:", t)

def on_Release(t):
	"""
	funcion como controlador, iniciaria nuestras funciones 
	y hara algo con el valor obtenido del time
	"""
	print("Liberado: ", round(t,2))

def get_time_onseconds(time1, time2):
	deltaTime = time2 - time1
	return deltaTime.total_seconds()

button.on_press = on_Press
button.on_release = on_Release

while True:
	time.sleep(1)
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

		elapse = press-release
		if elapse.total_seconds() (2/baseSecTimer):
			codeString += '-'
			print("Tu string: {},  ahora lleva una - mas".format(codeString))
			pin_String(codeString)
		elif elapse.total_seconds() < (1/baseSecTimer):
			codeString += '.'
			print("Tu string: {},  ahora lleva una . mas".format(codeString))
			pin_String(codeString)
		else:
			print("Nose que pusiste")
			pin_String(codeString)
	return codeString 

