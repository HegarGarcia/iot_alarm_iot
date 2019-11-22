import time
from grove.grove_button import GroveButton
from grove.grove_led import GroveLed
from grove.factory import Factory
from datetime import datetime as dt
from morseDict import MORSE_CODE_DICT

import threading
# import os
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes, hmac

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
	global onProcess
	print("Starting Morse Detector")
	time.sleep(2)
	print("Please press button to start submit your 4-digit pin")
	onProcess = True

def get_Ping_Code(t):
	global codeString
	if len(pinCode) < 4:
		print "Ping Code: {}, Llevas {}/4 digitos de tu PIN".format(pinCode, len(pinCode))
		pin_String(t)
		##validate after adding user signal (dot or dash)
		if len(codeString) == 5:
			#string valida, sino volvemos a iterar
			if codeString in MORSE_CODE_DICT.values():
				pinConvertido = MORSE_CODE_DICT.keys()[MORSE_CODE_DICT.values().index(codeString)]
				pinCode.append(pinConvertido)
				print "Se finalizo el numero! MORSE STRING: {}, NUMERO CONVERTIDO: {}".format(codeString, pinConvertido)
				codeString = ''
			else:
				print("Pin no valido, repetir digitos!")
				codeString = ''
	else:
		time.sleep(1.5)
		print "Validando Tu PIN: " + str(pinCode)
		check_pincode()

def pin_String(t):
	global codeString
	if len(codeString) < 5:
		print "\n\nEvaluando tiempo...\n\tTiempo pasado: " + str(round(t,3))
		if t >= (baseSecTimer - Tolerance) and t <= (baseSecTimer + Tolerance):
			codeString += '-'
			print("Tu string: {}, adding: -".format(codeString))
		elif t >= ((baseSecTimer * 3) - Tolerance) and t <= ((baseSecTimer * 3) + Tolerance):
			codeString += '.'
			print("Tu string: {}, adding: .".format(codeString))
		else:
			print("No pude detectar tu input")
		inicializar_blink()

def blink():
	led.on()
	time.sleep(Tolerance)
	led.off()
	time.sleep(Tolerance)
 
def inicializar_blink():
	threading.Thread(target=signal_to_user).start()

##Para feedback visual
def signal_to_user():
    for num in range(1, 3):
		led.on()
		time.sleep(0.1)
		led.off()
		time.sleep(0.1)

### Seccion de REQUESt COAP
def authenticate_method(pin):
    	"""
	Esta funcion simula la el controlador de la peticion COAP
	Nos regresa un dict, vacio si no encontro usuario con ese pin
	Objetivo: Obtener un matching con el PIN
	"""
	users = (
		{"name": "MIke", "pin_number": "4004"},
		{"name": "Maria", "pin_number":"5045"},
		{"name": "Moctzyma", "pin_number":"1029"},
		{"name": "Itzel", "pin_number":"3202"}
	)
	match = {}
	for user in users:
		if pin == user["pin_number"]:
			match = user
	return match

def check_pincode():
	global pinCode, onProcess
	"""
	Funcion para enviar peticion coap y hacer algo con la respuesta!
	Objetivo: Simular la peticion COAP Al servidor e imprime resultado!
	"""
	pinCodeMutation = list(pinCode)
	pin_code_toString = "".join(pinCodeMutation)
	if len(pin_code_toString) == 4:
		print "Pin code validated!"
		match = authenticate_method(pin_code_toString)
		if match:
			print "Welcome: {}, your pin code is:{}".format(match["name"], match["pin_number"])
		else:
			print "Authentication Failed, No se ha encontrado usuario con ese PIN"
		pinCode = []
		time.sleep(1)
		led.off()
		onProcess = False
	else:
		print "Invalid Pin!, try againg"
		pinCode = []
##controllers!!
def on_Press(t):
	"""
	funcion para imprimir current status
	"""

def on_Release(t):
	global onProcess
	"""
	funcion como controlador, iniciaria nuestras funciones 
	y hara algo con el valor obtenido del time
	"""
	print("Liberado: ", t)
	if not onProcess and t > 4:
		startEngine()
		blink()
	elif onProcess and len(pinCode) == 4 and t > 6:
		print("Apagando!")
		onProcess = False
		led.off()
		time.sleep(1)
	elif onProcess:
		get_Ping_Code(t)
	else:
		print("No entre!")
		led.on()
		time.sleep(0.4)
		led.off()
  
	print("ON proces:", onProcess)

button.on_press = on_Press
button.on_release = on_Release
#start script
while True:
	time.sleep(1)
	
