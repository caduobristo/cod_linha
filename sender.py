import socket
from funcoes import ami_encode, string_to_binary

def send_data(host='localhost', port=12345, data="Teste"):
    binary_string = string_to_binary(data)
    encoded_data = ami_encode(binary_string)
    print(f"Dado enviado: {data}\nDado binário: {binary_string}\nDados codificado: {encoded_data}")
    message = ' '.join(map(str, encoded_data))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode())

# Enviar os dados
send_data()
