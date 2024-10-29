import socket
import threading
from MasterServer import MasterServer

def handle_client(client_socket, master_server):
    """Função para lidar com as requisições de um cliente específico."""
    with client_socket:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            response = master_server.handle_command(data)
            client_socket.sendall(response.encode())
    print("Client disconnected.")

def start_server(host='localhost', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"MasterServer listening on {host}:{port}")

    master_server = MasterServer()

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected to client {address}")
        
        # Inicia uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, master_server))
        client_thread.start()

if __name__ == "__main__":
    start_server()
