import time
from grove.grove_button import GroveButton
from grove.grove_led import GroveLed
from grove.grove_pwm_buzzer import getGpioLookup, upmBuzzer
from grove.factory import Factory
from datetime import datetime as dt
from morseDict import MORSE_CODE_DICT_NUMBERS as MORSE_CODE_DICT
from coapReq import getUser

import threading
import sys
# import os
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes, hmac

mraa_pin = getGpioLookup("GPIO%02d" % 12)
button = GroveButton(5)
led = GroveLed(16)

chords = [upmBuzzer.BUZZER_DO, upmBuzzer.BUZZER_RE, upmBuzzer.BUZZER_MI,
		upmBuzzer.BUZZER_FA, upmBuzzer.BUZZER_SOL, upmBuzzer.BUZZER_LA,
		upmBuzzer.BUZZER_SI]

 
#setting variables for out login process
# base_time_seconds = input("Please select the timing beat in secs: ")
base_time_seconds = 0.3
tolerance =  base_time_seconds / 2.0
print("Timing base selected, now its {} secs".format(base_time_seconds))

pinCode= []
codeString = ''
onProcess = False

def changeProcess():
	global onProcess
	if onProcess:
		print"Closing Morse Detector, Deleting data...."
		time.sleep(1.5)
		print "Press any key to exit..."
		onProcess = False
	else:
		print("Starting Morse Detector...")
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
		if t >= (base_time_seconds - tolerance) and t <= (base_time_seconds + tolerance):
			codeString += '.'
			print("Tu string: {}, adding: .".format(codeString))
		elif t >= ((base_time_seconds * 2) - tolerance) and t <= ((base_time_seconds * 2) + tolerance):
			codeString += '-'
			print("Tu string: {}, adding: -".format(codeString))
		else:
			print("No pude detectar tu input")
		inicializar_blink()

##Para feedback visual
def blink():
	if onProcess:
		led.on()
		time.sleep(tolerance)
		led.off()
		time.sleep(tolerance)
 
def inicializar_blink():
	threading.Thread(target=signal_to_user).start()

def signal_to_user():
	for num in range(1, 3):
		led.on()
		time.sleep(0.1)
		led.off()
		time.sleep(0.1)

### Seccion de REQUESt COAP
def check_pincode():
	global pinCode
	"""
	Funcion para enviar peticion coap y hacer algo con la respuesta!
	Objetivo: Simular la peticion COAP Al servidor e imprime resultado!
	"""
	buzzer = upmBuzzer.Buzzer(mraa_pin)
 
	pinCodeMutation = list(pinCode)
	pin_code_toString = "".join(pinCodeMutation)
	if len(pin_code_toString) == 4:
		match = getUser(pin_code_toString)
		if match:
			print "\n\n\n \tWelcome: {}, your pin code is:{}".format(match['name'], match['pin_code'])
			for chord_ind in range (0,3):
				# play each note for a half second
				print(buzzer.playSound(chords[chord_ind], 500000))
				time.sleep(0.1)
		else:
			print "\n\n\n \tAuthentication Failed, No se ha encontrado usuario con ese PIN"
			for chord_ind in range (3,7):
				# play each note for a half second
				print(buzzer.playSound(chords[chord_ind], 900000))
				time.sleep(0.1)
		pinCode = []
		time.sleep(1)
		print "\n\t Saliendo del proceso..."	
		changeProcess()
	else:
		print "Invalid Pin!, try againg"
		pinCode = []

##controllers!!
def on_Press(t):
	"""
	funcion para imprimir current status
	"""

def on_Release(t):	
	"""
	funcion como controlador, iniciaria nuestras funciones 
	y hara algo con el valor obtenido del time
	"""
	print("Liberado: ", t)
	if not onProcess and t > 3:
		changeProcess()
		blink()
	elif onProcess and t > 8:
		print("Apagando!")
		changeProcess()
		led.off()
		time.sleep(1)
	elif onProcess:
		get_Ping_Code(t)
	else:
		print("No entre!")
		led.on()
		time.sleep(0.4)
		led.off()
  
	print("PROCESS STATUS: " + str(onProcess))

button.on_press = on_Press
button.on_release = on_Release

#start script
try:
	message = raw_input("\nPresiona cualquier tecla para salir...\n")
finally:
	print "Bye"	
