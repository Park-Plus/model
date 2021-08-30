
# Park+ ESP configuration file

"""

    Wi-Fi Settings
    
    Here, you need to put the Wi-Fi credentials in order for the 
    ESP module to be able to connect to your Wi-Fi network.

"""

WIFI_SSID = 'INSERT_YOUR_SSID_HERE'
WIFI_PASSWORD = 'INSERT_YOUR_WIFI_PASSWORD_HERE'


"""

    MQTT Settings
    
    Here, you need to put the MQTT details in order for the 
    ESP module to be able to connect to your MQTT server.

"""

MQTT_SERVER_ADDRESS = 'INSERT_YOUR_MQTT_SERVER_ADDRESS_HERE' # e.g. 10.0.0.15


"""

    Parking Settings
    
    Here, you need to put the settings for your specific parking structure

"""

ZONE_ID = 'INSERT_HERE_THE_PARKING_ZONE_ID' # Refers to the zone the ESP controls. e.g. Zone A -> Parking lots 1, 2, 3 - Zone B -> Parking lots 4, 5, 6
