import socket

class Client:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port

    def send_command(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(command.encode())
            response = client_socket.recv(4096).decode()  # Recebe resposta do servidor
            return response

def main():
    client = Client()
    print("Connected to the Distributed File System")
    print("Commands: upload, download, update, delete, view, activate, deactivate, logs, exit")

    while True:
        command = input("Enter command: ").strip().lower()
        if command == "exit":
            print("Exiting the system.")
            break
        response = client.send_command(command)
        print(response)

if __name__ == "__main__":
    main()
