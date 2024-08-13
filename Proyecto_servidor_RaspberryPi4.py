#Fernando Rivera Proyecto basado en control de luz segun la expresion facial inferida,
# codigo para Raspberry Pi 4 el es el servidor de este proyecto

import RPi.GPIO as GPIO
import socket

# Configurar los pines GPIO para el LED RGB
pin_r = 17
pin_g = 27
pin_b = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_r, GPIO.OUT)
GPIO.setup(pin_g, GPIO.OUT)
GPIO.setup(pin_b, GPIO.OUT)

def encender_led(r, g, b):
    GPIO.output(pin_r, r)
    GPIO.output(pin_g, g)
    GPIO.output(pin_b, b)

# Configurar el socket para la comunicación Ethernet
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 2020))
s.listen(10)
print("Servidor Iniciado, esperando conexiones") #Anuncio que se ha conectado al servidor el cliente

try:
    while True:
        (sc, addr) = s.accept()
        print("Conexión desde:", addr)
        while True:
            mensaje = sc.recv(64)
            if not mensaje:
                break
            comando = mensaje.decode().strip()

            if comando == '1':
                encender_led(GPIO.LOW, GPIO.LOW, GPIO.HIGH)  # AZUL / Enojo
                sc.send("LED Rojo encendido".encode())
            elif comando == '2':
                encender_led(GPIO.LOW, GPIO.HIGH, GPIO.LOW)  # VERDE / Felicidad
                sc.send("LED Verde encendido".encode())
            elif comando == '3':
                encender_led(GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)  # BLANCO / Neutral
                sc.send("LED Azul encendido".encode())
            elif comando == '4':
                encender_led(GPIO.HIGH, GPIO.HIGH, GPIO.LOW)  # AMARILLO / Tristeza
                sc.send("LED apagado".encode())
            elif comando == "quit":
                sc.send("Cerrando servidor...".encode())
                s.close()
                GPIO.cleanup()  # Limpiar la configuración de los pines GPIO
                break
            else:
                sc.send("Comando no reconocido".encode())
                print("Comando no reconocido:", comando)

        sc.close()
except KeyboardInterrupt:
    print("Servidor detenido manualmente")
finally:
    s.close()
    GPIO.cleanup()


