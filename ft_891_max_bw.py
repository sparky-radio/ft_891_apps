#!/usr/bin/env python3
"""
Yeasu FT-891 Max BW
Sets the radio's BW to 3k
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
    send_cat_command("GT0")
    # AGC - set 0 == fixed / 2 == 'MID'
    send_cat_command("GT02")

    print("Getting current frequency")
    # Get current frequency
    send_cat_command("FA")

    print("Setting current frequency")
    # Set Frequency to 14.200 MHz (FA command requires frequency in Hz)
    # The command should be 14200000;
    send_cat_command("FA014200000")

    print("Setting USB")
    # Set Mode to USB (MD command with parameters)
    # MD03; sets VFO A mode to USB
    send_cat_command("MD0C")

    # RX Audio Bandwidth - SH / 0 == fixed / 1 == on / 17 == 3 KHz
    # Read current
    print("Getting current BW")
    send_cat_command("SH0")
    print("Setting BW")
    # Write update
    send_cat_command("SH0117")
    print("Getting current BW")
    # Read current
    send_cat_command("SH0")


    # Read Radio Status - returns: 0 == 'RS' / 0 == normal / 1  == menu
    send_cat_command("RS")

    # Turn PTT ON (TX ON)
    # The 'TX' command is not standard; PTT is typically controlled differently,
    # often through a specific sequence or DTR/RTS lines via software like FLrig.
    # For a direct command for TX, you can use the 'TX' command (e.g., TX1; for ON) 
    # but check the manual as it can be mode dependent.

    # Example of toggling Break-In for CW (BI command) - Requires CW operation
    send_cat_command("BI1") # Break-In ON

    time.sleep(2)

    # Turn PTT OFF (if applicable)
    # send_cat_command("TX0")

    send_cat_command("BI1") # Break-In ON
    # Turn Break-In OFF
    send_cat_command("BI0")

except Exception as e:
    print(f"Could not open serial port: {e}")

finally:
    if ser.isOpen():
        ser.close()
        print("Serial port closed.")


