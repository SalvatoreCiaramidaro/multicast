import socket

def main():
    # Chiede all'utente l'indirizzo IP del server
    server_ip = input("Inserisci l'indirizzo IP del server: ")
    # Crea un socket per il client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connette il client al server
    client.connect((server_ip, 5000))

    # Riceve il prompt del server per il nickname
    prompt = client.recv(1024).decode('utf-8')
    nickname = input(prompt)
    client.send(nickname.encode('utf-8'))

    ciclo = True

    while ciclo:
        # Legge il messaggio da inviare al server
        messaggio = input("Inserisci il messaggio da inviare: ")
        # Invia il messaggio al server
        client.send(messaggio.encode('utf-8'))
        if messaggio.upper() == "QUIT":
            ciclo = False
        else:
            # Riceve la risposta dal server
            risposta = client.recv(1024).decode('utf-8')
            print(f"Risposta del server: {risposta}")

    client.close()

if __name__ == "__main__":
    main()