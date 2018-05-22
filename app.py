#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import serial,time,MFRC522,signal
import RPi.GPIO as GPIO


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()




@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

#Leitor do QR Code
@socketio.on('QRCode7980g')
def read_qr():
   print('Requisitou QRCode 7980g')
   try:
       Obj_porta = serial.Serial('/dev/ttyACM0', 9600)
       qrcode =  Obj_porta.readline(6)
   except serial.SerialException:
       qrcode = 'ERRO QRCode'
   emit('QRCode7980g', {'data': qrcode})
   print (qrcode)

#Leitor da balanca
@socketio.on('balanca_2098')
def getBalanca_2098():
   print('reqisitou Peso Balanca Toledo_2098')
   while 1:
      try:
          Port_bal = serial.Serial('/dev/ttyUSB0',9600)
          bal = Port_bal.readline(7)
          time.sleep(0.25)
      except serial.SerialException:
          bal = 'ERRO Balanca nao conectada'
      emit('balanca_2098',{'data': bal})
      print (bal)

#Leitor do cartao de Usuario
@socketio.on('cardUser')
def Get_Card_User():
   
   print('Requisitou Cartao Usuario')
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
	  emit('cardUser',{'data': id_card})
	  print (id_card)
          continue_reading = False
          GPIO.cleanup()

    

@socketio.on('disconnect_request')
def disconnect_request():
    print('Cliente Pediu Para Desconectar')
    emit('disconect',
         {'data': 'Voce foi Desconectado!'})
    print ('Cliente foi Desconectado!')
    disconnect()


#Conexao com o Cliente
@socketio.on('connect')
def test_connect():
    print ('Cliente Pediu para Conectar')
    emit('connect', {'data': 'Connected'})
    print ('Cliente conectado',request.sid)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    emit('disconect',
         {'data': 'Voce foi desconectado!'})

    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', port = '3000', debug=True)
