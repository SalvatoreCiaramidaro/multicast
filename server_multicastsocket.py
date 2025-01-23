import socket
import threading

def gestisci_client(socket_client, indirizzo):
    ciclo = True
    while ciclo:
        try:
            # Riceve il messaggio dal client
            messaggio = socket_client.recv(1024).decode('utf-8')
            if messaggio == "QUIT":
                ciclo = False
            print(f"Ricevuto {indirizzo}: {messaggio}")
            # Invia una conferma al client
            socket_client.send(f"Messaggio ricevuto".encode('utf-8'))
        except:
            ciclo = False
    socket_client.close()

def main():
    # Crea un socket per il server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associa il socket all'indirizzo e alla porta
    server.bind(('0.0.0.0', 5000))
    # Il server inizia ad ascoltare le connessioni in arrivo
    server.listen(2)
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server in ascolto su {server_ip} sulla porta 5000")

    while True:
        # Accetta una nuova connessione
        socket_client, indirizzo = server.accept()
        print(f"Connessione accettata da {indirizzo}")
        # Crea un nuovo thread per gestire il client
        gestore_client = threading.Thread(target=gestisci_client, args=(socket_client, indirizzo))
        gestore_client.start()

if __name__ == "__main__":
    main()