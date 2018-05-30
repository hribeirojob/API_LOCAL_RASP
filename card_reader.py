#!/usr/bin/env python

import MFRC522

def leitor_mfrc522():

   continue_reading = True
   while continue_reading:

       MIFAREReader = MFRC522.MFRC522()

      # Detecta o cartao
       (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

      # Se um cartao for encontrado!
       if status == MIFAREReader.MI_OK:

      # Pega o UID do cartao
          (status,uid) = MIFAREReader.MFRC522_Anticoll()

      # Se conseguir o  UID do cartao, continue
       if status == MIFAREReader.MI_OK:
          id_card =  str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])
	  return(id_card)
	  continue_reading = False
          GPIO.cleanup()
