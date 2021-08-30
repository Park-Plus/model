#!/usr/bin/python
# -*- coding: utf-8 -*-
import ujson

pins = {
    'A1': 2,
    'A2': 0,
    'A3': 4,
    'A4': 5,
    'A5': 16,
    }

led_maps = {
    'A1': [0, 1],
    'A2': [2, 3],
    'A3': [4, 5],
    'A4': [6, 7],
    'A5': [8, 9],
    }
parks = {}
statuses = {}

ready = False
loading = False
isWaitingForStatuses = False


def connect_and_subscribe():
    global client_id, mqtt_server, loading
    loading = True
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print 'Connected to %s MQTT broker.' % mqtt_server
    loading = False
    return client


def sub_cb(topic, msg):
    global statuses, isWaitingForStatuses, ready
    print 'Incoming data: ' + str(msg)

    dataJSON = ujson.loads(msg)

    if isWaitingForStatuses and dataJSON['type'] == 'statusesRequest':
        for (key, value) in dataJSON['data'].items():
            statuses[key] = value
        ready = True
        isWaitingForStatuses = False
        setup_pins()
    if dataJSON['type'] == 'setBooked':
        statuses[dataJSON['data']['park']] = 2
    if dataJSON['type'] == 'setFree':
        statuses[dataJSON['data']['park']] = 0


def restart_and_reconnect():
    loading = True
    print 'Failed to connect to MQTT broker. Reconnecting...'
    time.sleep(10)
    loading = False
    machine.reset()


def getStatuses():
    global statuses, topic_pub, isWaitingForStatuses
    payload = {'type': 'statusesRequest'}
    client.publish(topic_pub, ujson.dumps(payload))
    isWaitingForStatuses = True


def correctValue(current):
    if current == 2:
        return 2
    else:
        return int(not bool(current))


def statusNumberToString(status):
    if status == 0:
        return 'free'
    elif status == 1:
        return 'occupied'
    else:
        return 'booked'


def reportStateChange(statuses):
    global topic_pub
    payload = {'type': 'statusUpdate', 'data': statuses}
    client.publish(topic_pub, ujson.dumps(payload))
    print ujson.dumps(payload)


def setup_pins():
    global pins, parks
    for i in pins:
        print str(pins[i]) + ' set'
        sensor = machine.Pin(pins[i], machine.Pin.IN)
        parks[i] = sensor
        if statuses[i] == 1:
            np[led_maps[i][0]] = (16, 0, 0)
            np[led_maps[i][1]] = (16, 0, 0)
        elif statuses[i] == 0:
            np[led_maps[i][0]] = (0, 16, 0)
            np[led_maps[i][1]] = (0, 16, 0)
        else:
            np[led_maps[i][0]] = (0, 0, 16)
            np[led_maps[i][1]] = (0, 0, 16)
        np.write()


if __name__ == '__main__':
    try:
        client = connect_and_subscribe()
    except OSError, e:
        restart_and_reconnect()
    getStatuses()
    p4 = machine.Pin(12)
    servo = machine.PWM(p4, freq=50)
    servo.duty(100)

while True:
    client.check_msg()
    if ready:
        current_statuses = {}
        for i in pins:
            current_statuses[i] = correctValue(parks[i].value())
        currentLed = 0
        statesChanged = []
        for i in pins:
            if current_statuses[i] != statuses[i]:
                if statuses[i] == 2:
                    if current_statuses[i] == 1:
                        statuses[i] = current_statuses[i]
                else:
                    newState = {'park': i,
                                'newStatus': statusNumberToString(current_statuses[i])}
                    statesChanged.append(newState)
                    statuses[i] = current_statuses[i]
                if statuses[i] == 1:
                    np[led_maps[i][0]] = (16, 0, 0)
                    np[led_maps[i][1]] = (16, 0, 0)
                elif statuses[i] == 0:
                    np[led_maps[i][0]] = (0, 16, 0)
                    np[led_maps[i][1]] = (0, 16, 0)
                else:
                    np[led_maps[i][0]] = (0, 0, 16)
                    np[led_maps[i][1]] = (0, 0, 16)
            np.write()
        if len(statesChanged) > 0:
            reportStateChange(statesChanged)
    time.sleep(1)

while True and loading:
    for i in range(10):
        np[i] = (80, 80, 80)
        if i + 1 <= 9:
            np[i + 1] = (80, 80, 80)
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
