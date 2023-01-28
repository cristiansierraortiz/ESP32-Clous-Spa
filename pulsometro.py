from machine import sleep, SoftI2C, Pin, I2C, ADC  # Importamos el módulo machine
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import utime

led = Pin(2, Pin.OUT)


class Pulso():
	def __init__(self):
		self.datos = 0
		self.datos2 = 0
		self.datos3 = 0


def muestra(self):

  i2c = SoftI2C(sda=Pin(19),
                scl=Pin(23),
                freq=400000)
  sensor = MAX30102(i2c=i2c)

  if sensor.i2c_address not in i2c.scan():
    print("Sensor no encontrado.")
    return

  elif not (sensor.check_part_id()):
    print("ID de dispositivo I2C no correspondiente a MAX30102 o MAX30105.")
    return

  else:
    print("Sensor conectado y reconocido.")

    print("Configurando el sensor con la configuración predeterminada.", '\n')
    sensor.setup_sensor()
    sensor.set_sample_rate(400)
    sensor.set_fifo_average(8)
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
    sleep(1)
    dato3 = (sensor.read_temperature())  # ("Leyendo temperatura en °C.", '\n')
    self.datos3 = dato3
    compute_frequency = True
    print("Iniciando la adquisición de datos de los registros RED e IR...", '\n')
    sleep(1)
    t_start = ticks_us()
    samples_n = 0

    intervalos = [1, 2, 3]
    for i in intervalos:
      sensor.check()
      if sensor.available():
        red_reading = sensor.pop_red_from_storage()
        # ("Sensor_R",red_reading, "Sensor_IR", ir_reading)
        ir_reading = sensor.pop_ir_from_storage()
        f_conversion = 60/17500
        dato = (ir_reading*f_conversion)*1.5
        self.datos = dato  # ("BPM",dato)
        utime.sleep(1)

        dato2 = (red_reading*f_conversion)*1.8
        self.datos2 = dato2  # ("SpO2",dato2)
        utime.sleep(1)

        if compute_frequency:
          if ticks_diff(ticks_us(), t_start) >= 999999:
            f_HZ = samples_n
            samples_n = 0  # ("Adquiriendo frecuencia = ", f_HZ)
            t_start = ticks_us()
          else:
            samples_n = samples_n + 1

        print("El valor de BPM es: " + str(dato))
        print("El valor de SpO2 es: " + str(dato2))
        print("El valor de Temp es: " + str(dato3))
        print("Intento " + str(i) + " realizado")

    print("El valor de BPM final es: " + dato)
    print("El valor de SpO2 final es: " + dato2)
