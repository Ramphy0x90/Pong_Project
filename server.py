import socket
import sys
import time
from _thread import *


def socketbuild():
    # Funzione per mettere in ascolot il server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("SERVER_IP", 4445))
        # Accetto al massimo 2 client
        sock.listen(2)

        return sock
    except Exception:
        print("Socket error")
        return None


referSize = None

scoreA, scoreB = 0, 0
subScoreA, subScoreB = 0, 0
match = 1

playersCount = 0

# Dizionario con i dati iniziali dei giocatori e la partita. Punteggi, posizioni etc
positions = {
    0: "200;200;345;195;0;0;0;0;1;0",
    1: "200;200;345;195;0;0;0;0;1;1"
}

# Variabili per controllare i punteggi o l'esistenza di 2 giocatori
checkA, checkB, checkPlayers = True, True, True


def threaded_client(conn, p):
    global playersCount, positions, scoreA, scoreB, subScoreA, subScoreB, checkA, checkB, checkPlayers, referSize, match
    conn.send(str(p).encode())
    referSize = conn.recv(1024).decode().split(";")
    playersCount += 1

    while True:
        try:
            data = conn.recv(4096).decode()
            temp = data.split(";")

            # Aggiorno la lista con i nuovi punteggi da inviare
            temp[4] = str(scoreA)
            temp[5] = str(scoreB)
            temp[6] = str(subScoreA)
            temp[7] = str(subScoreB)
            temp[8] = str(match)

            if not data:
                break
            else:
                id = int(data.split(";")[-1])

                if playersCount == 2 and checkPlayers:
                    # Controllo se la palla ha toccato il muro di destra
                    if int(data.split(";")[2]) >= (int(referSize[0]) - int(referSize[2])) and checkA:
                        scoreA += 1
                        # Se lo score arriva a N punti il punteggio viene risettato e si incrementa la variabile
                        # che segna in quale partita ci si trova
                        if scoreA == 2:
                            subScoreA += 1
                            match += 1
                            scoreA, scoreB = 0, 0
                        checkA = False
                    if int(data.split(";")[2]) <= 0 and checkB:
                        scoreB += 1
                        if scoreB == 2:
                            subScoreB += 1
                            match += 1
                            scoreA, scoreB = 0, 0
                        checkB = False

                    # Se la palla supera una delle 2 meta una variabile viene risettata
                    # Questo per evitare che si possano fare 10 punti in un colpo se la palla rimbalza piu volte
                    if int(data.split(";")[2]) < int(referSize[0]) // 2:
                        checkA = True
                    if int(data.split(";")[2]) > int(referSize[0]) // 2:
                        checkB = True

                # Controllo se esiste un vincitore per poi inviare i dati ai client
                # Quando si invia -2 come ultimo valore significa che la partita è finita
                if subScoreA == 3:
                    positions = {0: "20;200;345;195;0;0;0;0;1;-2", 1: "670;200;345;195;0;0;0;0;1;-2"}
                elif subScoreB == 3:
                    positions = {0: "20;200;345;195;0;0;0;0;2;-2", 1: "670;200;345;195;0;0;0;0;2;-2"}

                # Controlllo se esiste solo un giocatore presente
                # Se un giocatore esce dal gioco viene mandato un segnale. -1 come ultimo parametro
                # e vengono risettati i punteggi
                if not checkPlayers:
                    positions = {0: "20;200;345;195;0;0;0;0;1;-1", 1: "670;200;345;195;0;0;0;0;1;-1"}
                    scoreA, scoreB = 0, 0
                    subScoreA, subScoreB = 0, 0
                    match = 1

                # Creo una stringa con i nuovi dati da inviare
                newData = ";".join(temp)

                # Viene usato l'id del cliente come chiave per inserire i dati
                positions[int(data.split(";")[-1])] = newData

                # QUa controllo l'id dei cliente per decidere quale stringa di dati inviare.
                # Questo per non avere sovvraposizioni di oggetti nel gioco.
                # Il giocatore 1 riceve solo i dati del giocatore 2 e lo stesso per il giocatore 2. Il contrario
                reply = positions[0 if id == 1 else 1]

                print(reply)

                conn.send(reply.encode())

                # Se vince un giocatore i punteggi vengono risettati
                if temp[-1] == "-2":
                    scoreA, scoreB = 0, 0
                    subScoreA, subScoreB = 0, 0
                    match = 1

        except:
            conn.close()
            break

    scoreA, scoreB = 0, 0
    playersCount -= 1
    checkPlayers = False
    print("Lost connection")

    # Quando un giocatore esce vengono risettati i valore nel modo iniziale
    # Senza inviare nessun segnale ai client
    time.sleep(1)
    checkPlayers = True
    positions = {0: "20;200;345;195;0;0;0;0;1;0", 1: "670;200;345;195;0;0;0;0;1;1"}
    scoreA, scoreB = 0, 0
    subScoreA, subScoreB = 0, 0
    match = 1

    print("Server ready")

    conn.close()


sock = socketbuild()

while True:
    try:
        # Accetto le varie connessioni che arrivano
        conn, addr = sock.accept()
        print("Connected to:", addr)

        # Inizio un nuovo thread per ogni connessione
        start_new_thread(threaded_client, (conn, playersCount))
    except KeyboardInterrupt:
        print("Server going down")
        sock.close()
        sys.exit(1)
