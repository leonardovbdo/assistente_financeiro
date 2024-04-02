import serial

PORTA_0 = "/dev/ttyACM0" # COM1
PORTA_1 = "/dev/ttyACM1" # COM2
PORTA_2 = "/dev/ttyACM2" # COM3

COMANDO_LIGAR = b'L' 
COMANDO_DESLIGAR = b'D' 

def iniciar_lampada(porta = PORTA_0):
    porta = serial.Serial(port=porta, baudrate=9600, bytesize=8, timeout=2, 
        stopbits=serial.STOPBITS_ONE)

    return porta

def atuar_sobre_a_lampada(acao, objeto, porta):
    if acao in ["ligar", "acender"] and objeto == "lâmpada":
        porta.write(COMANDO_LIGAR)
    elif acao in ["desligar", "apagar"] and objeto == "lâmpada":
        porta.write(COMANDO_DESLIGAR)
