import socket
import string
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def ami_encode(data):
    last_positive = True
    encoded = ''

    for bit in data:
        if bit == '0':
            encoded += '0'
        elif bit == '1':
            if last_positive:
                encoded += '1'
            else:
                encoded += '-1'
            last_positive = not last_positive
    
    return encoded

def ami_decode(data):
    decode = ''

    for bit in data:
        if bit == '0':
            decode += '0'
        elif bit == '1':
            decode += '1'

    return decode

def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    return binary

def binary_to_string(binary):
    string = ''.join(chr(int(binary[byte:byte+8], 2)) for byte in range(0, len(binary), 8))
    return string

def encrypt_decrypt(string, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(string))

def decodifica_mensagem(msg: str, key: str):
    msg_decod = ami_decode(msg)
    msg_crypt = binary_to_string(msg_decod)
    msg_original = encrypt_decrypt(msg_crypt, key)

    proc_decod = f"Mensagem recebida: {msg}\nMensagem decodificada: {msg_decod}\nMensagem criptografada: {msg_crypt}\nMensagem original: {msg_original}\n"

    return proc_decod

def codifica_mensagem(msg: str):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(random.choice(caracteres) for _ in range(10))
    msg_crypt = encrypt_decrypt(msg, key)
    msg_binaria = string_to_binary(msg_crypt)
    msg_codificada = ami_encode(msg_binaria)

    proc_cod = f"Mensagem: {msg}\nMensagem criptografada: {msg_crypt}\nMensagem binária: {msg_binaria}\nMensagem codificada: {msg_codificada}\n"

    return msg_codificada, key, proc_cod

def send_data(host: str, port: str, msg: str, text_area, frame):
    msg_codificada, key, proc_cod = codifica_mensagem(msg)
    data = f"{msg_codificada}|{key}"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(data.encode())
            update_text_area(proc_cod, text_area)
            plot_waveform(data, frame, "Forma de onda do dado enviado!")
    except ConnectionRefusedError:
        update_text_area("Conexão negada!", text_area)
    
def update_text_area(decoded_message, text_area):
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, decoded_message + '\n')

def plot_waveform(message, frame, titulo):
    wave = []

    for i in range(len(message)):
        if message[i] == '1' and message[i-1] != '-':
            wave.append(1)
        elif message[i] == '0':
            wave.append(0)
        elif message[i] == '-':
            i += 1
            wave.append(-1)
    
    if hasattr(plot_waveform, 'fig'):
        ax = plot_waveform.ax
        ax.clear()
    else:
        plot_waveform.fig, ax = plt.subplots()
        plot_waveform.ax = ax

    x = np.linspace(0, len(wave)-1, 10*len(wave))
    ax.step(x, np.repeat(wave, 10), where='mid')

    ax.set_ylim([-1.5, 1.5])
    ax.set_title(titulo)
    
    if hasattr(plot_waveform, 'canvas'):
        plot_waveform.canvas.draw()
    else:
        plot_waveform.canvas = FigureCanvasTkAgg(plot_waveform.fig, master=frame)
        plot_waveform.canvas.draw()
        plot_waveform.canvas.get_tk_widget().pack(pady=5)

def pega_ip():
    hostname = socket.gethostname()
    ip_adress = socket.gethostbyname(hostname)
    return ip_adress