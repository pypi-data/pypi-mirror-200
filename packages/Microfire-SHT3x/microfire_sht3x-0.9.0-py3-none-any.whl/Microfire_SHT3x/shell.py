#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
if int(str(range(3))[-2]) == 2:
  sys.stderr.write("You need python 3.0 or later to run this script\n")
  exit(1)

import cmd
from Microfire_SHT3x import Microfire_SHT3x
sht30 = Microfire_SHT3x()

class SHT3xShell(cmd.Cmd):
        prompt = '> '

        def do_measure(self, _):
                """take and display all measurements"""
                sht30.measure();
                print("{:.2f}".format(sht30.tempC), end='')
                print(" °C")
                print("{:.2f}".format(sht30.tempF), end='')
                print(" °F")
                print("{:.2f}".format(sht30.RH), end='')
                print(" %RH")
                print("{:.2f}".format(sht30.vpd_kPa), end='')
                print(" VPD kPa")
                print("{:.2f}".format(sht30.dew_pointC), end='')
                print(" dew point °C")
                print("{:.2f}".format(sht30.dew_pointF), end='')
                print(" dew point °F")

                if sht30.status:
                        print_red(sht30.status_string[sht30.status])

def print_red(txt): print("\033[91m {}\033[00m" .format(txt)) 
def print_green(txt): print("\033[92m {}\033[00m" .format(txt)) 

sht30.begin()
SHT3xShell().cmdloop()
