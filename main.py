from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
import network
import time
import urequests
import framebuf
import ujson
import pulsometro
from pulsometro import Pulso

##########################################
# Variables ESP32

anchoOLED = 128
altoOLED = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(anchoOLED, altoOLED, i2c)
led_Rojo = Pin(13, Pin.OUT)
led_Verde = Pin(26, Pin.OUT)
led_Amarillo = Pin(25, Pin.OUT)
led_Azul = Pin(33, Pin.OUT)
led_Naranja = Pin(32, Pin.OUT)

##########################################
# Variables
# =======================================================================

valor = i2c.scan()
validarConexionPantalla = str(valor)

##########################################
# Funciones

# funcion para importar logo en formato pbm
# =======================================================================


def buscar_icono(ruta):
    dibujo = open(ruta, "rb")
    dibujo.readline()
    xy = dibujo.readline()
    x = int(xy.split()[0])
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

# funcion para conectar la ESP32 a internet por WIFI
# =======================================================================


def conectaWifi(red, password):
    global miRed
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():  # Si no está conectado…
        miRed.active(True)  # activa la interface
        miRed.connect(red, password)  # Intenta conectar con la red
        print('Conectando a la red', red + "…")
        timeout = time.time()
        while not miRed.isconnected():  # Mientras no se conecte..
            if (time.ticks_diff(time.time(), timeout) > 10):
                return False
    return True

# funcion para mostrar mnesajes en la OLED
# =======================================================================


def mostrarOled(p1='', p2='', p3='', p4='', p5='', p6=''):
    oled.fill(0)
    oled.show()
    time.sleep(2)
    oled.text(p1, 20, 0)
    oled.text(p2, 20, 10)
    oled.text(p3, 20, 20)
    oled.text(p4, 20, 30)
    oled.text(p5, 20, 40)
    oled.text(p6, 20, 50)
    oled.show()
    time.sleep(5)

# funcion para limpiar mnesajes en la OLED
# =======================================================================


def limpiarOled():
    time.sleep(5)
    oled.fill(1)
    oled.show()
    time.sleep(3)
    oled.fill(0)
    oled.show()

# funcion para encender / apagar LED
# =======================================================================


def procesoLED(nomLED, parEncApg):
    nomLED.value(parEncApg)

# funcion para accionar el ServoMotor
# =======================================================================


def accionarServoMotor(ang1, ang2, ang3, servoParam):
    if servoParam == 1:
        servo = PWM(Pin(23), freq=50)
        angulos = [ang1, ang2, ang3]

        def map_s(x):
            return int((x - 0) * (2400000 - 500000) / (180 - 0) + 500000)
        for i in angulos:
            m = map_s(i)
            servo.duty_ns(m)
            time.sleep(1)
    elif servoParam == 2:
        servo2 = PWM(Pin(14), freq=50)
        angulos = [ang1, ang2, ang3]

        def map_s(x):
            return int((x - 0) * (2400000 - 500000) / (180 - 0) + 500000)
        for i in angulos:
            m = map_s(i)
            servo2.duty_ns(m)
            time.sleep(1)


# funcion para realizar peticiones HTTP (GET, POST, PUT, DELETE, etc)
# =======================================================================

def peticionHTTP(urlIn, param, peticion, qry='', qry2='', qry3=''):
    if peticion == 'GET':
        url = "https://clous-spa.fly.dev/api/v1/" + str(urlIn) + str(param)
        respuesta = urequests.get(url)
        return respuesta
    elif peticion == 'POST':
        url = "https://clous-spa.fly.dev/api/v1/" + str(urlIn)
        respuesta = urequests.post(
            url+"idCliente="+str(qry)+"&saturacion="+str(qry2)+"&ritmoCardiaco="+str(qry3))
        return respuesta
    elif peticion == 'EXTERNO':
        url = urlIn
        respuesta = urequests.get(url)
        return respuesta

# funcion para procesar Cromoterapia
# =======================================================================


def procesoColor(color):
    if color == "Verde":
        procesoLED(led_Verde, 1)
        time.sleep(2)
        mostrarOled('', '', 'Color', color, 'Activado!', '')
    elif color == "Azul":
        procesoLED(led_Azul, 1)
        time.sleep(2)
        mostrarOled('', '', 'Color', color, 'Activado!', '')
    elif color == "Amarillo":
        procesoLED(led_Amarillo, 1)
        time.sleep(2)
        mostrarOled('', '', 'Color', color, 'Activado!', '')
    elif color == "Naranja":
        procesoLED(led_Naranja, 1)
        time.sleep(2)
        mostrarOled('', '', 'Color', color, 'Activado!', '')

# funcion para procesar Aromaterapia
# =======================================================================


def procesoAroma(aroma):
    if aroma == "Manzanilla":
        print("Se ha activado el aroma a Manzanilla")
        mostrarOled('', '', 'Aroma', aroma, 'Activado!', '')
        intervalos = [1, 2, 3]
        for i in intervalos:
            accionarServoMotor(0, 180, 0, 1)
            mostrarOled('', 'Disparo', str(i), 'Aroma', 'Accionado', '')
            print("Disparo " + str(i) + " accionado correctamente")
            oled.fill(0)
            oled.show()
            time.sleep(1)
    elif aroma == "Canela":
        print("Se ha activado el aroma a Canela")
        mostrarOled('', '', 'Aroma', aroma, 'Activado!', '')
        intervalos = [1, 2, 3]
        for i in intervalos:
            accionarServoMotor(0, 180, 0, 2)
            mostrarOled('', 'Disparo', str(i), 'Aroma', 'Accionado', '')
            print("Disparo " + str(i) + " accionado correctamente")
            oled.fill(0)
            oled.show()
            time.sleep(1)

# funcion para procesar Musicoterapia
# =======================================================================


def procesoGeneroMusical(genero_musical):
    if genero_musical == "Instrumental":
        urlIn = "https://maker.ifttt.com/trigger/Instrumental/with/key/bYgdF-b0LXlI1hUQl-l9N0"
        mostrarOled('', '', 'Realizando', 'peticion', 'Espere...', '')
        respuesta = peticionHTTP(urlIn, '', 'EXTERNO')
        code = respuesta.status_code
        respuesta.close()

        if code == 200:
            print("La canción se esta reproduciendo...")
            mostrarOled('', '', 'Reproduciendo', 'Cancion', 'Spotify...', '')
        else:
            print("La canción no se pudo reproducir")
            mostrarOled('', '', 'Reproducion', 'Cancion', 'Fallida', '')

# funcion para validar y procesar el estado de la cita del cliente
# =======================================================================


def validarEstadoCita():
    mostrarOled('', 'Sesion', 'SPA', 'en', 'Curso', '')
    urlIn = "obtener-id-cita-cliente-reciente"
    respuesta = peticionHTTP(urlIn, '', 'GET')
    datos = ujson.loads(respuesta.text)
    id_cita_proxima = datos['datos'][0]['min']
    respuesta.close()
    urlIn = "validar-estado-cita-cliente/"
    respuesta = peticionHTTP(urlIn, id_cita_proxima, 'GET')
    datos = ujson.loads(respuesta.text)
    estado_cita_proxima = datos['datos'][0]['estado_cita']
    respuesta.close()
    time.sleep(2)

    while estado_cita_proxima == False:
        print("aun no termina la cita")
        time.sleep(2)
        print("se ejecuta la peticion HTTP")
        urlIn = "validar-estado-cita-cliente/"
        respuesta = peticionHTTP(urlIn, id_cita_proxima, 'GET')
        datos = ujson.loads(respuesta.text)
        estado_cita_proxima = datos['datos'][0]['estado_cita']
        code = respuesta.status_code
        respuesta.close()
        time.sleep(2)

        if estado_cita_proxima == True:
            respuesta.close()
            mostrarOled('', '', 'Sesion', 'Finalizada', '', '')
            urlIn = "https://maker.ifttt.com/trigger/Encuesta/with/key/cepUlBpq1XyHvLxcmpwVIi"
            mostrarOled('', '', 'Realizando', 'peticion', 'Espere...', '')
            respuesta = peticionHTTP(urlIn, '', 'EXTERNO')
            code = respuesta.status_code

            if code == 200:
                print("Encuesta enviada con éxito")
                mostrarOled('', '', 'Encuesta', 'Enviada!', '', '')
                respuesta.close()

                leds = [led_Verde, led_Rojo,
                        led_Amarillo, led_Azul, led_Naranja]
                for i in leds:
                    procesoLED(i, 0)
                mostrarOled('', '', 'Leds', 'Apagados', '', '')
                limpiarOled()
            else:
                print(
                    "Encuesta no ha sido enviada, favor validar")
                mostrarOled('', 'Encuesta', 'No',
                            'Enviada', 'Favor', 'Validar')
                respuesta.close()

                limpiarOled()
                time.sleep(1)

# funcion para procesar la terapia
# =======================================================================


def procesoTerapia(urlIn, param, peticion):
    mostrarOled('', '', 'Realizando', 'peticion', 'Espere...', '')
    respuesta = peticionHTTP(urlIn, param, peticion)
    datos = ujson.loads(respuesta.text)
    nombre_terapia = datos['datos']['descripcion_terapia']
    color = datos['datos']['color']['nombre_color']
    aroma = datos['datos']['aroma']['nombre_aroma']
    genero_musical = datos['datos']['genero']['nombre_genero_musical']

    mostrarOled('', 'Terapia ' + str(param), nombre_terapia,
                'Aplicada', 'Correctamente', '')

    procesoGeneroMusical(genero_musical)
    procesoColor(color)
    procesoAroma(aroma)
    validarEstadoCita()


##########################################
# Proceso General
# =======================================================================

# realiza el saludo


mostrarOled('', '', 'Bienvenido', 'Clous', 'Spa', '')

# valida conexión de la OLED

if validarConexionPantalla == "[60]":
    print("Pantalla conectada correctamente")

    # se conecta a la red WIFI

    if conectaWifi("CASA 300-2.4", "Casa300*"):
        print("Conexión exitosa!")
        print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
        mostrarOled('', '', 'Conexion', 'Exitosa!', 'WIFI', '')
        urlIn = "obtener-id-cita-cliente-reciente"
        mostrarOled('', '', 'Realizando', 'peticion', 'Espere...', '')
        respuesta = peticionHTTP(urlIn, '', 'GET')
        datos = ujson.loads(respuesta.text)
        id_cita_proxima = datos['datos'][0]['min']
        respuesta.close()
        urlIn = "obtener-cita-cliente-reciente/"
        respuesta = peticionHTTP(urlIn, id_cita_proxima, 'GET')
        datos = ujson.loads(respuesta.text)
        code = respuesta.status_code
        respuesta.close()

        if code == 200:
            id_cliente = datos['datos'][0]['id_cliente_cita']
            nombre_cliente = datos['datos'][0]['nombres_cliente']
            apellido_cliente = datos['datos'][0]['primer_apellido_cliente']

            # muestra el nombre del cliente

            mostrarOled('', '', 'Bienvenid@',
                        nombre_cliente, apellido_cliente, '')

            # captura los datos del oximetro

            mostrarOled('', '', 'Leyendo', 'Datos', 'Sensor', '')
            oximetro = Pulso()
            mostrarOled('', 'Coloca', 'Dedo', 'en el', 'Sensor', '')
            mostrarOled('Favor', 'No', 'Levantar',
                        'Dedo', 'Leyendo', 'Datos...')
            oximetro.muestra()
            mostrarOled('', '', 'Puede', 'Levantar', 'Dedo', '')

            BPM = oximetro.datos
            print("El valor final de BPM es: " + str(BPM))
            SpO2 = oximetro.datos2
            print("El valor final de SpO2 es: " + str(SpO2))

            if SpO2 == 0 or BPM == 0:
                print("No hay datos del sensor")
                mostrarOled('', 'No', 'Hay', 'Datos', 'Sensor', '')
            else:
                # muestra datos del sensor en la OLED

                ST = "Sat:" + str(SpO2) + " SpO2"
                RC = "Rit:" + str(BPM) + " BPM"
                mostrarOled('', 'Datos', 'Sensor', ST, RC, '')

                # inserta datos del sensor en la BD

                urlIn = "insertar-datos-cita-cliente?"
                mostrarOled('', '', 'Realizando', 'peticion', 'Espere...', '')
                respuesta = peticionHTTP(
                    urlIn, '', 'POST', id_cliente, int(SpO2), int(BPM))
                code = respuesta.status_code
                respuesta.close()
                print(respuesta.status_code)

                if code == 200:
                    mostrarOled('', 'Datos', 'insertados',
                                'correctamente', 'BD', '')
                else:
                    mostrarOled('', 'Datos', 'No', 'insertados',
                                'favor', 'validar!')

                # valida los datos del sensor y aplica la terapia configurada, segun BPM

                if BPM <= 90:
                    print("Ritmo bajo")
                    mostrarOled('', '', 'Resultado', 'Ritmo bajo', '', '')
                    urlIn = "obtener-terapia/"
                    param = 1

                    procesoTerapia(urlIn, param, 'GET')

                elif BPM >= 90 and BPM <= 95:
                    print("Ritmo medio")
                    mostrarOled('', '', 'Resultado', 'Ritmo medio', '', '')
                    urlIn = "obtener-terapia/"
                    param = 2

                    procesoTerapia(urlIn, param, 'GET')

                else:
                    print("Ritmo alto")
                    mostrarOled('', '', 'Resultado', 'Ritmo alto', '', '')
                    urlIn = "obtener-terapia/"
                    param = 3

                    procesoTerapia(urlIn, param, 'GET')

        else:
            print("No existen citas pendientes para hoy")
            mostrarOled('', 'No', 'Hay', 'Citas', 'Pendientes', '')
            limpiarOled()

    else:
        print("Imposible conectar")
        miRed.active(False)
        mostrarOled('', 'Sin', 'Conexion', 'a', 'WIFI', '')
        limpiarOled()
