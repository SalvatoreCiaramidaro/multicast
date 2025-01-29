import socket
import threading

# Dizionario per tenere traccia dei client connessi e i loro nickname
clienti = {}
# Dizionario per mappare gli indirizzi IP ai nickname
ip_nickname = {}

def gestisci_client(socket_client, indirizzo):
    ciclo = True
    nickname = ""
    client_ip = indirizzo[0]
    try:
        if client_ip in ip_nickname:
            nickname = ip_nickname[client_ip]
            socket_client.send(f"Ben tornato, {nickname}! Inserisci il tuo messaggio: ".encode('utf-8'))
            clienti[socket_client] = nickname
            print(f"{indirizzo} ha riconnesso il nickname {nickname}")
        else:
            # Riceve il nickname del client
            socket_client.send("Inserisci il tuo nickname: ".encode('utf-8'))
            nickname = socket_client.recv(1024).decode('utf-8').strip()
            ip_nickname[client_ip] = nickname
            clienti[socket_client] = nickname
            print(f"{indirizzo} ha impostato il nickname su {nickname}")
        
        while ciclo:
            try:
                # Riceve il messaggio dal client
                messaggio = socket_client.recv(1024).decode('utf-8').strip()
                if messaggio.upper() == "QUIT":
                    ciclo = False
                elif messaggio.upper() in ["L", "LIST"]:
                    # Invia la lista degli utenti connessi
                    lista_utenti = ", ".join(clienti.values())
                    socket_client.send(f"Utenti connessi: {lista_utenti}".encode('utf-8'))
                else:
                    print(f"Ricevuto da {nickname}: {messaggio}")
                    # Invia una conferma al client
                    socket_client.send("Messaggio ricevuto".encode('utf-8'))
            except:
                ciclo = False
    except:
        pass
    finally:
        socket_client.close()
        if socket_client in clienti:
            print(f"{clienti[socket_client]} si è disconnesso.")
            del clienti[socket_client]

def main():
    # Crea un socket per il server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associa il socket all'indirizzo e alla porta
    server.bind(('0.0.0.0', 5000))
    # Il server inizia ad ascoltare le connessioni in arrivo
    server.listen(5)
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