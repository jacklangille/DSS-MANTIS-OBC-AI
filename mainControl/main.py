# UART comm is on port /dev/ttys002
# Brew install socat
# In one terminal run socat -d -d pty,raw,echo=0 pty,raw,echo=0
# In another terminal run ~ % echo "WAKE" > /dev/ttys004

import serial
import logging
import logging.handlers


log_file = "uart_communication.log"
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

log_handler = logging.handlers.RotatingFileHandler(
    log_file, mode="a", maxBytes=1e6, backupCount=5
)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

PORT = "/dev/ttys003"
BAUD_RATE = 9600
WAKE = "1"
SLEEP = "2"
RECEIVE = "3"
LOAD_MODEL = "4"
PREPROCESS = "5"
INFERENCE = "6"
TRANSMIT = "7"


def load_model():
    logging.info("Initializing model...")


def receive_image(data):
    logging.info("Receiving and storing image...")


def preprocess_images():
    logging.info("Beginning image processing...")


def perform_inference():
    logging.info("Beginning image inference...")


def send_results():
    logging.info("Sending back inference results...")


def wake():
    logging.info("Waking up...")


def sleep():
    logging.info("Entering low power mode...")


def listen():
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
        logging.info("Listening on port: %s", PORT)
        while True:
            try:
                if ser.in_waiting > 0:
                    incoming_data = ser.readline().decode().strip()
                    logging.info("Received data: %s", incoming_data)
                    if incoming_data == WAKE:
                        wake()
                    elif incoming_data == SLEEP:
                        receive_image(incoming_data)
                    elif incoming_data == RECEIVE:
                        preprocess_images()
                    elif incoming_data == LOAD_MODEL:
                        load_model()
                    elif incoming_data == PREPROCESS:
                        preprocess_images()
                    elif incoming_data == INFERENCE:
                        perform_inference()
                    elif incoming_data == TRANSMIT:
                        send_results()
            except serial.SerialException as e:
                logging.error("Serial error: %s", e)
                break
            except Exception as e:
                logging.error("An error occurred: %s", e)
                break


if __name__ == "__main__":
    listen()
