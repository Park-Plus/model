import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

IN1 = 6  # IN1
IN2 = 13  # IN2
IN3 = 19  # IN3
IN4 = 26  # IN4

time = 0.001

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)


def Step1():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.output(IN4, True)
    sleep(time)
    GPIO.output(IN4, False)


def Step2():
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.output(IN4, True)
    GPIO.output(IN3, True)
    sleep(time)
    GPIO.output(IN4, False)
    GPIO.output(IN3, False)


def Step3():
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.output(IN3, True)
    sleep(time)
    GPIO.output(IN3, False)


def Step4():
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    sleep(time)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)


def Step5():
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.output(IN2, True)
    sleep(time)
    GPIO.output(IN2, False)


def Step6():
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.output(IN1, True)
    GPIO.output(IN2, True)
    sleep(time)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)


def Step7():
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.output(IN1, True)
    sleep(time)
    GPIO.output(IN1, False)


def Step8():
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.output(IN4, True)
    GPIO.output(IN1, True)
    sleep(time)
    GPIO.output(IN4, False)
    GPIO.output(IN1, False)


def left(step):
    for i in range(step):
        Step1()
        Step2()
        Step3()
        Step4()
        Step5()
        Step6()
        Step7()
        Step8()


def right(step):
    for i in range(step):
        Step8()
        Step7()
        Step6()
        Step5()
        Step4()
        Step3()
        Step2()
        Step1()


GPIO.cleanup()
