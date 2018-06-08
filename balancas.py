#!/usr/bin/env python

#balancas Toledo
#testes executados em modelos 2098, 9094c
import time
import serial

def balanca_toledo_v1():
   try:
      Port_bal = serial.Serial('/dev/ttyUSB0',9600)
      bal = Port_bal.readline(7)[1:7]
      time.sleep(0.25)
   except serial.SerialException:
       bal = 'ERRO'
   return(bal)

