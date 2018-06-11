#!/usr/bin/env python

import serial

#Leitor Honeywell 7980g
def honeywell_7980g(): 
   try:
      Obj_porta = serial.Serial('/dev/ttyACM0', 9600)
      qrcode =  Obj_porta.readline(7)
   except serial.SerialException:
      qrcode = 'error500'
   return(qrcode)   