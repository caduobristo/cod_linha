import socket
from funcoes import ami_decode, binary_to_string

def start_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Servidor ouvindo em {host}:{port}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Conectado por {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Dados codificado recebido: {data.decode()}")
                decode_data = ami_decode(data.decode())
                print(f"Dados decodificado: {decode_data}")
                string_data = binary_to_string(decode_data)
                print(f"Dados recebido: {string_data}")

# Executar o servidor
start_server()
