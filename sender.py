from common_imports import *

def string_to_binary(string):
    binary = ''.join(format(ord(char), '08b') for char in string)
    return binary

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
            plot_waveform(data, frame, "0 de onda do dado enviado!", root)
    except ConnectionRefusedError:
        update_text_area("Conexão negada!", text_area)

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