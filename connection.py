import socket


class Connection:
    """
    La classe connection serve per gestire la connessione tra i client e il server
    """
    def __init__(self, refersize):
        """
        Nel costruttore riceve come unico parametro una stringa con dei valori
        """

        # Creo un socket per IPV4 e connessione in TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.refersize = refersize
        self.id = None

    def serverConnect(self):
        """Funzione per collegarmi al server e per controllare se una connessione puo essere stabilita"""
        try:
            self.sock.connect(("SERVER_IP", 4445))
            # Ricevo dal server un id per poi interpretare i dati ricevuti dal'altro giocatore
            self.id = self.sock.recv(1024).decode()
            self.sock.send(self.refersize.encode())
            return True
        except Exception:
            return False

    def serverDisconnect(self):
        """Funzione per scollegarmi in modo sicuro dal server di gioco"""
        self.sock.close()

    def sendData(self, prya, pryb, positionball, scorea, scoreb, subscorea, subscoreb, match):
        """Funzione per inviare dati al server. Riceve i dati separatamente per poi creare una stringa"""
        yA = prya   # Paddle A Rect Y
        yB = pryb   # Paddle B Rect Y
        xBall = positionball.x
        yBall = positionball.y

        try:
            self.sock.send((str(yA) + ";" +
                            str(yB) + ";" +
                            str(xBall) + ";" +
                            str(yBall) + ";" +
                            str(scorea) + ";" +
                            str(scoreb) + ";" +
                            str(subscorea) + ";" +
                            str(subscoreb) + ";" +
                            str(match) + ";" +
                            self.id).encode())

        except BrokenPipeError:
            print("Server Down")
        except OSError:
            pass

    def reciveData(self):
        """
        Funzione per ricevere i dati. Riceve dal server una stringa e poi viene trasformata in una lista
        per essere utilizzata dal client
        """
        return (self.sock.recv(1024).decode()).split(";")
