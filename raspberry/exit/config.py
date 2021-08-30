# Park+ Raspberry Pi (exit) configuration file

"""

    OpenALPR Settings
    
    Here, you need to put the config files for OpenALPR in order for it to fetch your license
    and runtime data.

"""

OPENALPR_REGION = "eu"
OPENALPR_LICENSE = "PATH_TO_OPENALPR_LICENSE"
OPENALPR_RUNTIME_DATA = "PATH_TO_OPENALPR_RUNTIME_DATA"


"""

    MQTT Settings
    
    Here, you need to put the MQTT details in order for the 
    ESP module to be able to connect to your MQTT server.

"""

MQTT_SERVER_ADDRESS = "INSERT_YOUR_MQTT_SERVER_ADDRESS_HERE"  # e.g. 10.0.0.15
