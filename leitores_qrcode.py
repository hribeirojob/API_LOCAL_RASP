#!/usr/bin/env python

import serial

#Leitor Honeywell 7980g
def honeywell_7980g():
   try:
      Obj_porta = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
      qrcode =  Obj_porta.read(5)
   except serial.SerialException:
      qrcode = 'error500'
   Obj_porta.close()
   return(qrcode)

