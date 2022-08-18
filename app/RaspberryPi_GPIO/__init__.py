# __init__.py
# This file is used to send GPIO commands to Raspberry Pi

# Raspberry Pi GPIO framework
import RPi.GPIO as GPIO
import time
import spidev
from lib_nrf24 import NRF24
import time


class GPIO_Commands:
    # Initialize Pins as outputs
    def __init__(self):
        GPIO.setwarnings(False)

        # Set GPIO Mode
        GPIO.setmode(GPIO.BCM)
        
        # !! Change this to reflect the API's GPIO pins
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)

        self.pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
        self.ackMessg = [4]
        self.ackMessgLen = 2
        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(0, 17, 4000000)
        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x76)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_MAX)
        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()
        self.radio.openReadingPipe(1, self.pipes[1])
        self.radio.openWritingPipe(self.pipes[0])
        self.radio.printDetails()

    # Toggle a Pin HIGH or LOW
    def TogglePin(self, pin, status):
        if status == 0:
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.HIGH)

    def CommunicateWithArduino(self, device_name, pipe_address, status):
        # Open Writing Pipe
        self.radio.openWritingPipe(pipe_address)

        # prevent a message being sent larger than 32 bits by making it a list
        sendMessage = list(device_name + " " + str(status))

        # Prepare the Message in string form with only the first 32 letters
        while(len(sendMessage) < 32):
            sendMessage.append(0)

        # Send the Message
        self.radio.write(sendMessage)






