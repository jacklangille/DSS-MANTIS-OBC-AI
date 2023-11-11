# UART comm is on port /dev/ttys002
# Brew install socat
# In one terminal run socat -d -d pty,raw,echo=0 pty,raw,echo=0
# In another terminal run ~ % echo "WAKE" > /dev/ttys003

import serial
import os
import time

PORT = "/dev/ttys002"
BAUD_RATE = 9600
WAKE_COMMAND = "WAKE"
SLEEP_COMMAND = "SLEEP"


def wake():
    print("Waking up...")


def sleep():
    print("Entering low power mode...")


def listen():
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
        print("Listening...")
        while True:
            if ser.in_waiting > 0:
                incoming_data = ser.readline().decode().strip()
                if incoming_data == WAKE_COMMAND:
                    wake()
                if incoming_data == SLEEP_COMMAND:
                    sleep()


if __name__ == "__main__":
    listen()
