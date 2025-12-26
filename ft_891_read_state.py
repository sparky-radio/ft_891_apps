#!/usr/bin/env python3
"""
Yeasu FT-891 Reads Current State
"""

import serial
import time
from datetime import datetime, timezone, UTC
import sys


# Configure the serial port
# Replace 'COM5' with the actual port name found in your device manager
# (e.g., '/dev/ttyUSB0' on Linux, 'COM3' on Windows, '/dev/tty.usbmodem' on macOS)
ser = serial.Serial(
    port='/dev/ttyUSB0', 
    baudrate=19200,          # Must match the radio's CAT RATE menu setting
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1               # Timeout in seconds
)

def send_cat_command(command):
    """Sends a CAT command to the radio."""
    # Yaesu commands must end with a semicolon
    cmd_string = command + ';'
    try:
        ser.write(cmd_string.encode('ascii'))
        print(f"Sent: {cmd_string.strip()}")
        
        # You may want to read the response if needed
        response = ser.readline().decode('ascii').strip()
        if response:
            print(f"Received: {response}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Error: {e}")



try:
    ser.isOpen()
    print("Serial port opened successfully.")

    # Example Commands:
    # Get ID 650 == FT-891
    send_cat_command("ID")

    # AGC - read current
    print('AGC Setting')
    send_cat_command("GT0")

    # Information
    print('IF - Information')
    send_cat_command("IF")






except Exception as e:
    print(f"Could not open serial port: {e}")

finally:
    if ser.isOpen():
        ser.close()
        print("Serial port closed.")
