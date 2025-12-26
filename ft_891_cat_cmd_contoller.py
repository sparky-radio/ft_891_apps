#!/usr/bin/env python3
"""
Yeasu FT-891 Sends CAT 
"""

import csv
import serial
import time
from datetime import datetime, timezone, UTC
import sys

class FT891CatCommandController:

    def __init__(self, csv_file='./commands.csv', port='/dev/ttyUSB0', baudrate=19200):

        # Configure the serial port
        # Replace 'COM5' with the actual port name found in your device manager
        # (e.g., '/dev/ttyUSB0' on Linux, 'COM3' on Windows, '/dev/tty.usbmodem' on macOS)
        self.serial = serial.Serial(
            port, 
            baudrate,          # Must match the radio's CAT RATE menu setting
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1               # Timeout in seconds
        )
        self.commands = self.load_commands(csv_file)

    def load_commands(self, csv_file):
        commands = {}
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                commands[row['function_name']] = row
        return commands
    
    def send_command(self, function_name, param=None):
        if function_name not in self.commands:
            raise ValueError(f"Unknown function: {function_name}")
        
        cmd_info = self.commands[function_name]
        command = cmd_info['command']
        description = cmd_info['description']
        print(f"Sending {description}")
        
        if param:
            full_command = f"{command}{param};"
        else:
            full_command = f"{command};"
        
        self.serial.write(full_command.encode('ascii'))
        response = self.serial.readline().decode('ascii').strip()
   
        if response.startswith(command) :
            return response.removeprefix(command)
        
        return response


    

rig = FT891CatCommandController('commands.csv')
freq = rig.send_command('get_vfo_a_freq')
print(f"VFO-A frequency {freq}")

id = rig.send_command('get_identification')
print(f"get_identification {id}")
