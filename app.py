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
@socketio.on('QRCode7980g', namespace='/test')
def read_qr():
   try:
       Obj_porta = serial.Serial('/dev/ttyACM0', 9600)
       valor =  Obj_porta.readline(6)
   except serial.SerialException:
       valor = 'ERRO'
   emit('resposta', {'data': [valor]})
   print (valor)

#Leitor da balanca
@socketio.on('balanca_2098', namespace='/test')
def getBalanca_2098():
   while 1:
      try:
          Port_bal = serial.Serial('/dev/ttyUSB0',9600)
          bal = Port_bal.readline(7)
          time.sleep(0.25)
      except serial.SerialException:
          bal = 'ERRO'
      emit('resposta',{'data': [bal]})
      print (bal)

#Leitor do cartao de Usuario
@socketio.on('cardUser', namespace='/test')
def Get_Card_User():

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
	  emit('resposta',{'data': [id_card]})
	  print (id_card)
          continue_reading = False
          GPIO.cleanup()

    

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('resposta',
         {'data': 'Voce desconectou!'})
    print ('Cliente desconectou!')
    disconnect()


#Conexao com o Cliente
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})
    print ('Cliente conectado',request.sid)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    emit('resposta',
         {'data': 'Voce foi desconectado!'})

    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=True)
