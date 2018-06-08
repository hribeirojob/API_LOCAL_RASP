# API_LOCAL_RASP
Api em Socket-IO que faz comunicação com as portas seriais de um Raspberry

Este repositorio tem a finalidade de  fazer comunicação com as portas seriais do Raspberry Pi 3 onde serao plugados os seguintes equipamentos

 Balaça Toledo
 Leitor de QR-Code
 Modulo Arduino de leitura de cartao RFID de curta distancia (RFID-RC522)

Todos esses modulos estao dispostos separadamente com um arquivo para cada um
unidos por um arquivo principal que monta tudo em sockets para disponibilização do usuario

Requisitos para funcionamento

Python2.7 - Python-pip - Flask - Flask-Socket-IO - PySerial
  Abaixo os comandos para instalar os pacotes
# sudo apt-get install python-pip -y && sudo pip install flask-socketio && sudo apt-get install python2.7 && python -m pip install pyserial

Para instalar as dependencias que estao listadas dentro do arquivo requirements use o comando
$ pip install -r requirements.txt

Para o leitor de cartao RF-ID use o seguinte comando para clonar o modulo nescessário
# clone https://github.com/mxgxw/MFRC522-python

Temos que habilitar so SPI do Raspberry para isso siga os passos
No terminal digite

sudo raspi-config
Vá na opção 5 depois na P4 e habilite teclando no <YES>

