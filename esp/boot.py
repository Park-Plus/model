import time
import ubinascii
import machine
import micropython
import network
import esp
import neopixel
import ujson
import config
from umqttsimple import MQTTClient

esp.osdebug(None)
import gc
gc.collect()

ssid = config.WIFI_SSID
password = config.WIFI_PASSWORD

mqtt_server = config.MQTT_SERVER_ADDRESS

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = 'parks/' + str(config.ZONE_ID) + '/send'.encode()
topic_pub = 'parks/' + str(config.ZONE_ID) + '/rec'.encode()

station = network.WLAN(network.STA_IF)
station_ap = network.WLAN(network.AP_IF)

np = neopixel.NeoPixel(machine.Pin(14), 10)

station.active(True)
station.connect(ssid, password)

station_ap.active(False)
while station.isconnected() == False:
    print 'Connecting...'
    for i in range(10):
        np[i] = (0, 0, 16)
        if i + 1 <= 9:
            np[i + 1] = (0, 0, 16)
        np.write()
        time.sleep(0.05)
    time.sleep(1)
    for i in range(9, 0, -1):
        np[i] = (0, 0, 0)
        if i - 1 >= 0:
            np[i - 1] = (0, 0, 0)
        np.write()
        time.sleep(0.05)
    time.sleep(1)
    pass

print 'Connection successful'

for i in range(10):
    np[i] = (0, 0, 0)
    np.write()

print station.ifconfig()
