import time
import stepper
import threading
import requests
import json
import config
import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from openalpr import Alpr

thread = None
barOpen = False
alpr = Alpr(
    config.OPENALPR_REGION, config.OPENALPR_LICENSE, config.OPENALPR_RUNTIME_DATA
)


def detectStop(frame):
    stopHaarcascade = "plate.xml"
    signalCascade = cv.CascadeClassifier(stopHaarcascade)
    signal = signalCascade.detectMultiScale(frame, 1.05, 3)
    if len(signal) > 0:
        return True, signal[0]
    return False, [-1, -1, -1, -1]


def bar(threadname):
    global barOpen
    barOpen = True
    stepper.left(128)
    sleep(10)
    stepper.right(128)
    barOpen = False


def stopRec(image):
    global count, stop

    found, (x, y, w, h) = detectStop(image)
    if found:
        if not stop:
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            count += 1
            cv.putText(
                image,
                "Found: YES",
                (25, 25),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 0, 0),
                2,
            )
            cv.putText(
                image,
                "Countdown: " + str(lim - count),
                (25, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2,
            )
        else:
            count = 0
    else:
        stop = False
        count = 0
        cv.putText(
            image, "Found: NO", (25, 25), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2
        )

    if (count == lim or stop) and barOpen == False:
        cv.imwrite("recognised_plate.jpg", image)
        results = alpr.recognize_file("recognised_plate.jpg")
        plate = results["results"][0]["plate"]
        requestBody = {"plate": plate}
        requests.post(config.BACKEND_ADDRESS + "/park/stay/start", data=requestBody)
        stop = True
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        barTH = threading.Thread(target=bar, args=(".",))
        barTH.start()


count = 0
stop = False
lim = 5

if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    for frame in camera.capture_continuous(
        rawCapture, format="bgr", use_video_port=True
    ):
        time.sleep(0.01)

        image = cv.flip(frame.array, -1)
        stopRec(image)
        cv.imshow("Original Image", image)

        rawCapture.truncate(0)

        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            cv.destroyAllWindows()
            exit()
