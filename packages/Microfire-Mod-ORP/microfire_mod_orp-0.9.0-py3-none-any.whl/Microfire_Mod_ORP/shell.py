#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
if int(str(range(3))[-2]) == 2:
  sys.stderr.write("You need python 3.0 or later to run this script\n")
  exit(1)

import cmd, inspect, math, sys
import Microfire_Mod_ORP
orp = Microfire_Mod_ORP.i2c()

fw_compatible = 1
hw_compatible = 1

class Mod_ORP_Shell(cmd.Cmd):
    intro="Type `help` for a list of commands\n`enter` repeats the last command"
    prompt = '> '

    def do_config(self, a):
        """prints out all the configuration data\nparameters: none"""
        print("Mod-ORP Config: ", end='')
        if orp.connected():
            print_green('connected')
            orp.getDeviceInfo()
            if (orp.fwVersion != fw_compatible) or (orp.hwVersion != hw_compatible):
                print_red("*This version of shell was designed for a different hardware revision or firmware version*")

            print("Calibration:")
            print(" single point: ", end='')
            if math.isnan(orp.calibrationSingleOffset):
                print("-")
            else:
                print("{:.2f}".format(orp.calibrationSingleOffset))

            print("hardware:firmware version: ", end='')
            print(orp.hwVersion, end='')
            print(":", end='')
            print(orp.fwVersion)
        else:
             print_red('**disconnected**')


    def do_reset(self, a):
        """reset all saved values\nparameters: none"""
        orp.reset()
        self.do_config(self)

    def do_orp(self, line):
        """starts an ORP measurement\nparameters: none"""
        orp.measureORP()

        print("{:.2f}".format(orp.mV), end='')
        print(" mV")

        if orp.status:
            print_red(orp.status_string[orp.status])

    def do_single(self, line):
        """Single point calibration\nparameters: solution_mV"""
        data = [s for s in line.split()]

        orp.calibrateSingle(float(data[0]), True)
        if orp.status:
            print_red(orp.status_string[orp.status])

        self.do_config(self)

    def do_i2c(self, line):
        """changes the I2C address"""
        i2c_address = int(line, 16)

        if ((i2c_address <= 0x07) or (i2c_address > 0x7f)):
            print("Error: I2C address not in valid range")
        else:
            orp.setI2CAddress(i2c_address);

    def do_exit(self, s):
        """Exits\nparameters: none"""
        return True

def print_red(txt): print("\033[91m {}\033[00m" .format(txt)) 
def print_green(txt): print("\033[92m {}\033[00m" .format(txt)) 

orp.begin()
Mod_ORP_Shell().cmdloop()