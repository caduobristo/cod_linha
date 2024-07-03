import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from funcoes import decodifica_mensagem, update_text_area, plot_waveform, pega_ip

def start_server(host: str, port: str):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    update_text_area("Servidor iniciado", text_area)

    def accept_connections():
        while True:
            conn, addr = server_socket.accept()
            data = conn.recv(4096).decode('utf-8')
            if data: 
                plot_waveform(data, frame, "Forma de onda do dado recebido!")
                msg, key = data.split('|')
                proc_decod = decodifica_mensagem(msg, key)
                update_text_area(proc_decod, text_area)
    
    thread = threading.Thread(target=accept_connections)
    thread.daemon = True
    thread.start()

def on_start_server_button():
    host = entry_host.get()
    port = int(entry_port.get())
    start_server(host, port)

def on_closing():
    plt.close()
    root.destroy()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Receiver")

frame = tk.Frame(root)
frame.pack(pady=20)

# Entrada para o IP do servidor
tk.Label(frame, text="IP do Servidor:").pack(pady=5)
entry_host = tk.Entry(frame, width=50)
entry_host.pack(pady=5)
entry_host.insert(0, pega_ip())

# Entrada para a porta do servidor
tk.Label(frame, text="Porta do Servidor:").pack(pady=5)
entry_port = tk.Entry(frame, width=50)
entry_port.pack(pady=5)
entry_port.insert(0, '65432')

# Botão para inciar servidor
btn_send_message = tk.Button(frame, text="Iniciar servidor", command=on_start_server_button)
btn_send_message.pack(pady=5)

# Área de texto para mostrar a mensagem decodificada recebida
tk.Label(frame, text="Mensagem decodificada recebida:").pack(pady=5)
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
text_area.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()