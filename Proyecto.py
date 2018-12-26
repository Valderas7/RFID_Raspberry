#!/usr/bin/env python
# -*- coding: utf8 -*-

# Importamos librerías y definimos variables
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from picamera import PiCamera
from sense_hat import SenseHat
R = [255, 0, 0]  # Rojo
G = [0, 255, 0]  # Verde

# Creamos objeto de Sense Hat y del RFID
sense=SenseHat()
MIFAREReader = MFRC522.MFRC522()

# Variable para hacer el bucle de lecturas de tarjetas RFID
lectura_continua = True

# Esto se ejecuta cuando se deja de leer tarjetas RFID con Control + C
def end_read(signal,frame):
    global lectura_continua
    print "Lectura finalizada"
    lectura_continua = False
    GPIO.cleanup()

# Para coger la señal
signal.signal(signal.SIGINT, end_read)

# Mensaje comienzo del proceso
print "Bienvenido"
print "Presiona Ctrl-C para parar el proceso\n"

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while lectura_continua:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # SI encontramos tarjeta, lo imprimimos por pantalla
    if status == MIFAREReader.MI_OK:
        print "Tarjeta detectada"
    
    # Obtener ID tarjeta
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # Si tenemos la ID, nos la imprime por pantalla
    if status == MIFAREReader.MI_OK:

        print "Lectura tarjeta User ID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
        # Congelamos tiempo 1s
        time.sleep(1)
        # Hacemos foto para ver quién está intentando acceder.
        # Creamos objeto de la PiCámara y la cerramos al final
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.rotation = 180
        camera.start_preview(fullscreen=False, window=(30,30,320,240))
        camera.capture('/home/pi/git/proyecto_asignatura/Proyecto/imagen.jpg')
        photo = open('/home/pi/git/proyecto_asignatura/Proyecto/imagen.jpg','rb')
        camera.close()

        # Si la tarjeta tiene el UID que buscamos se permite el acceso
        if uid[0] == 227 and uid[1] == 93 and uid[2] == 65 and uid[3] == 197:

            #Pantalla en verde
            question_mark = [
            G, G, G, G, G, G, G, G,
            G, G, G, G, G, G, G, G,
            G, G, G, G, G, G, G, G,
            G, G, G, G, G, G, G, G,
            G, G, G, G, G, G, G, G,
            G, G, G, G, G, G, G, G,
            G, G, G, G, G, G, G, G,
            G, G, G, G, G, G, G, G
            ]

            sense.set_pixels(question_mark)
            time.sleep(1)
            
            # Mensaje de bienvenida por pantalla y por Sense Hat
            print "Bienvenido a casa\n"
            sense.show_message('BIENVENIDO',text_colour=[100,100,100], scroll_speed = 0.05)
        
        else:
            # Si no tiene esa ID la Sense Hat entera en rojo
            question_mark = [
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R,
            R, R, R, R, R, R, R, R
            ]

            sense.set_pixels(question_mark)
            time.sleep(1)
            
            # Acceso denegado por pantalla y Sense Hat
            print "Error de autenticación\n"
            sense.show_message('ACCESO DENEGADO',text_colour=[100,100,100], scroll_speed = 0.05)

# ------------LECTURA SENSORES--------------------------



Humedad=sense.get_humidity()
Temp1=sense.get_temperature_from_humidity()
Temp2=sense.get_temperature_from_pressure()
Presion=sense.get_pressure()
print("Humedad: %2.3f" %Humedad)
print("Temperaturas: %2.3f %2.3f" % (Temp1,Temp2))
print("Presión: %4.2f" %Presion)

TStr=str(round(Temp1,2))
sense.show_message("T:"+TStr)
HStr=str(round(Humedad,2))
sense.show_message("H:"+HStr)
PStr=str(round(Presion,2))
sense.show_message("P:"+PStr)


# ----------------- SENSEHAT COLORES Y ESCRIBIR ----------------------------



sense.show_message('Hola,',text_colour=[100,100,100])
sense.show_message(nombre,scroll_speed=0.2, text_colour=[0,100,0])
time.sleep(1)
sense.clear()
    