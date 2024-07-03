import tkinter as tk
from tkinter import scrolledtext
from funcoes import send_data
import matplotlib.pyplot as plt

def on_send_message_button():
    host = entry_host.get()
    port = int(entry_port.get())
    msg = entry_message.get()

    send_data(host, port, msg, text_area, frame)

def on_closing():
    plt.close()
    root.destroy()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Sender")

frame = tk.Frame(root)
frame.pack(pady=20)

# Entrada para o IP do servidor
tk.Label(frame, text="IP do Servidor:").pack(pady=5)
entry_host = tk.Entry(frame, width=50)
entry_host.pack(pady=5)
entry_host.insert(0, '192.168.137.1')

# Entrada para a porta do servidor
tk.Label(frame, text="Porta do Servidor:").pack(pady=5)
entry_port = tk.Entry(frame, width=50)
entry_port.pack(pady=5)
entry_port.insert(0, '65432')

# Entrada para a mensagem
tk.Label(frame, text="Digite a Mensagem:").pack(pady=5)
entry_message = tk.Entry(frame, width=50)
entry_message.pack(pady=5)

# Botão para enviar a mensagem
btn_send_message = tk.Button(frame, text="Enviar Mensagem", command=on_send_message_button)
btn_send_message.pack(pady=5)

# Área de texto para mostrar a mensagem decodificada
tk.Label(frame, text="Mensagem Decodificada:").pack(pady=5)
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
text_area.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()