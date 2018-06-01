#!/usr/bin/env python

from threading import Lock
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
import time
######### Modulos proprios ############
from card_reader import leitor_mfrc522 
from leitores_qrcode import honeywell_7980g
from balancas import balanca_toledo_v1
#######################################


app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
seg_plano = None
thread_lock = Lock()
enviar_peso = 0

def getBalanca():
   global enviar_peso   
   while True:
      time.sleep(0.25)
      if enviar_peso == 1:
         peso = balanca_toledo_v1()
         socketio.emit('balanca_2098',{'data': peso})
         print (peso)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

#Leitor do QR Code
@socketio.on('QRCode7980g')
def read_qr():
   print('Requisitou QRCode 7980g')
   qrcode = honeywell_7980g()
   emit('QRCode7980g', {'data': qrcode})
   print (qrcode)

#Leitor da balanca
@socketio.on('balanca_2098')
def Balanca(entrada):
   global enviar_peso 
   enviar_peso = int(entrada)
   print ('Argumento do peso: ',enviar_peso)

#Leitor do cartao de Usuario
@socketio.on('cardUser')
def Get_Card_User():
   print('Usuraio requisitou o cartao RFID')
   id_card = leitor_mfrc522()
   emit('cardUser',{'data': id_card})
   print (id_card)

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
    global seg_plano
    with thread_lock:
        if seg_plano is None:
            seg_plano = socketio.start_background_task(target=getBalanca)
    emit('conectado', {'data': 'Voce esta conectado!'})
    print ('Cliente conectado',request.sid)

    
if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', port = '3000', debug=True)
