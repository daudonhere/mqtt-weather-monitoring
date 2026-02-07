from machine import Pin, I2C, PWM
import network
import time
import dht
import ujson
from umqtt.simple import MQTTClient

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

MQTT_CLIENT_ID = "esp32-weather-lcd"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "wokwi/weather"

TEMP_LOW = 25.0
TEMP_HIGH = 32.0

HUM_LOW = 40.0
HUM_HIGH = 70.0

sensor = dht.DHT22(Pin(15))

led_red = Pin(26, Pin.OUT)
led_blue = Pin(27, Pin.OUT)

buzzer = PWM(Pin(25))
buzzer.duty(0)

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

LCD_ADDR = 0x27
LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100
CMD = 0
DATA = 1

def lcd_write(value, mode):
    high = mode | (value & 0xF0) | LCD_BACKLIGHT
    low = mode | ((value << 4) & 0xF0) | LCD_BACKLIGHT
    i2c.writeto(LCD_ADDR, bytes([high | ENABLE]))
    i2c.writeto(LCD_ADDR, bytes([high]))
    i2c.writeto(LCD_ADDR, bytes([low | ENABLE]))
    i2c.writeto(LCD_ADDR, bytes([low]))

def lcd_cmd(cmd):
    lcd_write(cmd, CMD)

def lcd_data(data):
    lcd_write(data, DATA)

def lcd_init():
    time.sleep(0.05)
    lcd_cmd(0x33)
    lcd_cmd(0x32)
    lcd_cmd(0x28)
    lcd_cmd(0x0C)
    lcd_cmd(0x06)
    lcd_cmd(0x01)
    time.sleep(0.01)

def lcd_set_cursor(col, row):
    row_offsets = [0x80, 0xC0]
    lcd_cmd(row_offsets[row] + col)

def lcd_print(text):
    for c in text:
        lcd_data(ord(c))

lcd_init()
lcd_print("Connecting WiFi")

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(WIFI_SSID, WIFI_PASS)

while not sta.isconnected():
    time.sleep(0.2)

lcd_cmd(0x01)
lcd_print("WiFi Connected")

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.connect()

lcd_set_cursor(0, 1)
lcd_print("MQTT Connected")
time.sleep(2)

lcd_cmd(0x01)
lcd_print("Weather Monitor")

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()

    payload = ujson.dumps({
        "temperature": temp,
        "humidity": hum
    })
    client.publish(MQTT_TOPIC, payload)

    led_red.off()
    led_blue.off()
    buzzer.duty(0)

    alarm = False

    if temp < TEMP_LOW:
        led_blue.on()
        alarm = True
        temp_status = "COLD"
    elif temp > TEMP_HIGH:
        led_red.on()
        alarm = True
        temp_status = "HOT"
    else:
        temp_status = "SAFE"

    if hum < HUM_LOW:
        led_blue.on()
        alarm = True
        hum_status = "DRY"
    elif hum > HUM_HIGH:
        led_red.on()
        alarm = True
        hum_status = "WET"
    else:
        hum_status = "SAFE"

    if alarm:
        buzzer.freq(2000)
        buzzer.duty(512)

    lcd_set_cursor(0, 0)
    lcd_print("T:{:.1f}C H:{:.0f}%   ".format(temp, hum))

    lcd_set_cursor(0, 1)
    lcd_print("{:<8}{:<7}".format(temp_status, hum_status))

    time.sleep(2)
