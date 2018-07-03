#!/usr/bin/env python

from threading import Lock
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect, close_room, leave_room, join_room
import time
######### Modulos proprios ############
from card_reader import leitor_mfrc522
from leitores_qrcode import honeywell_7980g
from balancas import balanca_toledo_v1
#######################################



###############VARIAVEIS###############
app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
task_balanca = None
task_qrcode   = None
task_rfid   = None
thread_lock_peso = Lock()
thread_lock_qrcode = Lock()
thread_lock_rfid = Lock()
enviar_peso = 0
peso_anterior = 0
enviar_qr = 0
enviar_rfid = 0


def getBalanca():
   global enviar_qr
   global enviar_peso
   global enviar_rfid
   global peso_anterior

   while True:
      time.sleep(0.25)
      if enviar_peso == 1 and enviar_qr == 0 and enviar_rfid == 0:
         peso = balanca_toledo_v1()
         if peso_anterior != peso:
            socketio.emit('balanca_2098',{'data': peso})
            peso_anterior = peso
            print (peso)



def read_qr():
   global enviar_qr
   global enviar_peso
   global enviar_rfid

   while True:
      time.sleep(0.25)
      if enviar_qr == 1 and enviar_rfid == 0 and enviar_peso == 0:
         qrcode = honeywell_7980g()
         socketio.emit('QRCode7980g', {'data': qrcode})
         enviar_qr = 0
         print(qrcode)


def cartao_rfid():
    global enviar_qr
    global enviar_peso
    global enviar_rfid

    while True:
       time.sleep(0.25)
       if enviar_rfid == 1 and enviar_qr == 0 and enviar_peso == 0:
          id_card = leitor_mfrc522()
          socketio.emit('cardUser',{'data': id_card})
          print (id_card)
          enviar_rfid = 0

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)



#Socekt do QR Code
@socketio.on('QRCode7980g')
def read_qrcode():
   global enviar_qr
   global enviar_peso
   global enviar_rfid
   enviar_rfid = 0
   enviar_peso = 0
   enviar_qr = 1
   print('Requisitou QRCode 7980g')


#Socket da balanca
@socketio.on('balanca_2098')
def Balanca(entrada):
   global enviar_peso
   global enviar_qr
   global enviar_rfid
   enviar_peso = int(entrada)
   enviar_rfid = 0
   enviar_qr = 0
   if enviar_peso == 1:
      print ('Enviar peso:',enviar_peso)
   else:
      print ('Nao enviar peso:',enviar_peso)


#Socekt do cartao de Usuario
@socketio.on('cardUser')
def Get_Card_User():
   global enviar_qr
   global enviar_peso
   global enviar_rfid
   enviar_rfid = 1
   enviar_peso = 0
   enviar_qr = 0
   print('Usuraio requisitou o cartao RFID')


#Requisicao para desconectar
@socketio.on('disconnect_request')
def disconnect_request():
    print('Cliente Pediu Para Desconectar')
    emit('disconect',
         {'data': 'Voce foi Desconectado!'})
    disconnect()
    print('Client disconnected', request.sid)

#Conexao com o Cliente
@socketio.on('connect')
def test_connect():
    global task_balanca
    global task_qrcode
    global task_rfid
    with thread_lock_peso:
       if task_balanca is None:
          task_balanca = socketio.start_background_task(target=getBalanca)
    with thread_lock_qrcode:
       if task_qrcode is None:
          task_qrcode = socketio.start_background_task(target=read_qr)
    with thread_lock_rfid:
       if task_rfid is None:
          task_rfid = socketio.start_background_task(target=cartao_rfid)
    emit('conectado', {'data': 'Voce esta conectado!'})
    print ('Cliente conectado',request.sid)

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', port = '3000', debug=True)
