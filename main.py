import time
import pygame
import sys
from connection import Connection
from GameObjs.paddle import Paddle
from GameObjs.ball import Ball

pygame.init()

# Definire i colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (237, 237, 19)
RED = (255, 0, 0)
GREEN = (36, 171, 12)
BLUE = (14, 102, 179)

# Aprire(creare) la finestra del gioco
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# Creare la lista che contiene gli sprite
all_sprites_list = pygame.sprite.Group()

# Aggiungere gli sprite creati alla lista
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)


class Button:
    """"
    La classe button serve per creare bottoni. Viene usata solo nel menu principale
    """
    def __init__(self, color, x, y, width, height, text=''):
        """"
        Nel suo costruttore riceve il colore del background, posizione, grandezza ed il testo
        """
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.centerH = (size[0] / 2) - (self.x + self.width) / 2
        self.centerV = ((size[1] / 10) * 4.5) - (self.y + self.height) / 2

    def draw(self, win):
        """Funzione per disgnare un rettangolo in background per il testo"""
        pygame.draw.rect(win, self.color, (self.centerH, self.centerV, self.width, self.height), 0)

        # Carico file per la font
        font = pygame.font.Font("Data/coders_crux.ttf", 40)
        text = font.render(self.text, 1, WHITE)
        win.blit(text, text.get_rect(center=(self.centerH + self.width / 2, self.centerV + self.height / 2)))

    def changeColor(self, win, color):
        """Funzione per cambiare il colore del rettangolo del testo"""
        self.color = color
        self.draw(win)
        pygame.display.flip()

    def isOver(self, x, y):
        """funzione per controllare se la posizione del mouse è dentro il rettangolo del testo"""
        if x in range(int(self.centerH), int(self.centerH + self.width) + 1) and y in range(int(self.centerV), int(
                self.centerV + self.height) + 1):
            return True
        return False


createConection = True


def gameMenu():
    global createConection

    onMenu = True

    # Creare un oggetto connection per poi stabilire una connessione con il server
    connection = Connection(";".join([str(size[0]), str(size[1]), ball.getSize()[0]]))

    while onMenu:
        # Questa condizione è stata fatta per evitare di creare oggetti in loop in modo da non ranlentizzare il menu
        if createConection:
            connection = Connection(";".join([str(size[0]), str(size[1]), ball.getSize()[0]]))
            createConection = False

        mouseDown = False

        for event in pygame.event.get():  # individua un evento = l'utente ha fatto qualcosa
            if event.type == pygame.QUIT:  # l'utente vuole chiudere la finestra
                onMenu = False  # la condizione del loop viente cambiata, finisce il gioco
            elif event.type == pygame.KEYDOWN:  # evento usando la tastiera
                if event.key == pygame.K_x:  # il gioco finisce al click di X della tastiera
                    onMenu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Se l'utente schiaccia il bottone sul mouse una variabile
                mouseDown = True  # viene settata a True

        # Prendo le coordinate del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Funzione per centralizzare il testo in orizzontale
        textPosition = lambda text, y: text.get_rect(center=(size[0] / 2, (size[1] // 10) * y))

        screen.fill(BLACK)
        h1 = pygame.font.Font("Data/coders_crux.ttf", 60)
        h3 = pygame.font.Font("Data/coders_crux.ttf", 26)

        title = h1.render("Pong", 1, WHITE)
        caption = h3.render("Progetto finale per il modulo 122", 1, YELLOW)

        screen.blit(title, textPosition(title, 1.5))
        screen.blit(caption, textPosition(caption, 2.5))

        # Creo i vari bottoni per il menu e li disegno a schermo
        playB = Button(BLACK, 0, 0, 120, 45, "Gioca")
        playB.draw(screen)

        creditB = Button(BLACK, 0, -110, 120, 45, "Crediti")
        creditB.draw(screen)

        exitB = Button(BLACK, 0, -220, 120, 45, "Esci")
        exitB.draw(screen)

        # Controllo se il mouse è dentro il perimetro del rettangolo del testo
        # Se si, cambio il colore da nero a verde
        # Per ogni bottone controllo se il mouse viene schiacciato nelle coordinate dove si trova il bottone
        # Per poi chiamare una funzione
        if playB.isOver(mouse_x, mouse_y):
            playB.changeColor(screen, GREEN)
            if mouseDown:
                # Prima di iniziare il gioco controllo che il client si possa collegare al server
                if connection.serverConnect():
                    runGame(connection)
                    createConection = True
                else:
                    screen.fill(BLACK)
                    h1 = pygame.font.Font("Data/coders_crux.ttf", 45)
                    text = h1.render("Server di gioco offline. Attendere", 1, RED)
                    text_rect = text.get_rect(center=(size[0] / 2, size[1] / 2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    time.sleep(2)

        if creditB.isOver(mouse_x, mouse_y):
            creditB.changeColor(screen, GREEN)
            if mouseDown: creditsMenu()
        if exitB.isOver(mouse_x, mouse_y):
            exitB.changeColor(screen, GREEN)
            if mouseDown:
                connection.serverDisconnect()
                pygame.quit()
                sys.exit(0)

        pygame.display.flip()


def creditsMenu():
    onMenu = True

    while onMenu:
        mouseDown, mouseUp = False, False

        for event in pygame.event.get():  # individua un evento = l'utente ha fatto qualcosa
            if event.type == pygame.QUIT:  # l'utente vuole chiudere la finestra
                onMenu = False  # la condizione del loop viente cambiata, finisce il gioco
            elif event.type == pygame.KEYDOWN:  # evento usando la tastiera
                if event.key == pygame.K_x:  # il gioco finisce al click di X della tastiera
                    onMenu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True

        mouse_x, mouse_y = pygame.mouse.get_pos()
        textPosition = lambda text, y: text.get_rect(center=(size[0] / 2, (size[1] // 10) * y))

        screen.fill(BLACK)
        h1 = pygame.font.Font("Data/coders_crux.ttf", 60)
        h3 = pygame.font.Font("Data/coders_crux.ttf", 26)

        title = h1.render("Crediti", 1, YELLOW)
        caption = h3.render("Grazie al lavoro di gruppo tra Emilija Daceva e Ramphy Aquino Nova", 1, WHITE)
        caption_2 = h3.render("è stato possibile creare questo particolare progetto", 1, WHITE)

        screen.blit(title, textPosition(title, 1.5))
        screen.blit(caption, textPosition(caption, 2.5))
        screen.blit(caption_2, textPosition(caption_2, 3))

        returnB = Button(BLACK, 0, 0, 250, 45, "Torna al menu")
        returnB.draw(screen)

        if returnB.isOver(mouse_x, mouse_y):
            returnB.changeColor(screen, GREEN)
            if mouseDown: gameMenu()


# Schermata per visualizzare in quale partita ci si trova
def matchScreen(num):
    screen.fill(BLACK)
    h1 = pygame.font.Font("Data/coders_crux.ttf", 60)
    text = h1.render("Partita {}".format(num), 1, BLUE)
    text_rect = text.get_rect(center=(size[0] / 2, size[1] / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(1)


# Schermata per visualizzare il vincitore
def winPlayerScreen(playerid):
    screen.fill(BLACK)
    h1 = pygame.font.Font("Data/coders_crux.ttf", 45)
    text = h1.render("Vince il giocatore {}".format(playerid), 1, GREEN)
    text_rect = text.get_rect(center=(size[0] / 2, size[1] / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(1)


def runGame(connection):
    # Mi collego al server di gioco
    connection.serverConnect()

    # Condizione per il loop infinito del gioco
    carryOn = True

    # "Orario" per l'update del gioco (sprite, schermo)
    clock = pygame.time.Clock()

    # punteggio
    scoreA = 0
    scoreB = 0
    subScoreA = 0
    subScoreB = 0
    matchnum = 1
    refermatch = 1

    matchScreen(matchnum)

    while carryOn:
        for event in pygame.event.get():  # individua un evento = l'utente ha fatto qualcosa
            if event.type == pygame.QUIT:  # l'utente vuole chiudere la finestra
                carryOn = False  # la condizione del loop viente cambiata, finisce il gioco
                connection.serverDisconnect()  # Quando si esce dal gioco per andare nel menu ci si scollega dal server
            elif event.type == pygame.KEYDOWN:  # evento usando la tastiera
                if event.key == pygame.K_x:  # il gioco finisce al click di X della tastiera
                    carryOn = False
                    connection.serverDisconnect()

        # definizione dei movimenti delle paddle
        keys = pygame.key.get_pressed()
        # Connection.id è una variabile che gestisce l'id del giocatore,
        # viene data ad ogni nuova connesione con il server
        if keys[pygame.K_UP]:
            if connection.id == '0':
                paddleA.moveUp(5)
            elif connection.id == '1':
                paddleB.moveUp(5)
        if keys[pygame.K_DOWN]:
            if connection.id == '0':
                paddleA.moveDown(5)
            elif connection.id == '1':
                paddleB.moveDown(5)

        # --- update degli sprite
        all_sprites_list.update()

        # Controllare se la palla tocca una dei quattro muri
        if ball.rect.x >= (size[0] - int(ball.getSize()[0])):
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > (size[1] - int(ball.getSize()[0])):
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        # Controlla se la palla ha toccato una delle paddle
        if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
            ball.bounce()

        # Invio i dati per giocare al server tramite la l'oggetto connection
        connection.sendData(paddleA.rect.y, paddleB.rect.y, ball.rect, scoreA, scoreB, subScoreA, subScoreB,
                            str(matchnum))
        # Ricevo i dati per aggiornare lo shermo
        data = connection.reciveData()

        font = pygame.font.Font("Data/coders_crux.ttf", 40)
        messagePlayer = font.render("Giocatore 2 offline. Uscendo dal gioco", 1, WHITE)
        text_rect = messagePlayer.get_rect(center=(size[0] / 2, size[1] / 2))

        # Condizione per controllare se il giocatore 2 è uscito dalla partita
        # Se si, il giocatore rimanente viene rimandato nel menu principale
        if data[-1] == '-1':
            screen.fill(BLACK)
            screen.blit(messagePlayer, text_rect)
            pygame.display.flip()
            time.sleep(2)
            carryOn = False

        try:
            # Aggiorno i vari dati dei paddle, punteggi e pallina
            if connection.id == '0':
                paddleB.rect.y = int(data[1])
            elif connection.id == '1':
                paddleA.rect.y = int(data[0])

            if data[-1] != connection.id:
                scoreB = int(data[5])
                scoreA = int(data[4])
                subScoreA = int(data[6])
                subScoreB = int(data[7])

            if connection.id == '0':
                ball.rect.x = int(data[2])
                ball.rect.y = int(data[3])

            matchnum = int(data[8])

            # Controllo se la partita è finita per poi mostrare il vincitore
            if data[-1] == '-2':
                winPlayerScreen(data[8])
                connection.serverDisconnect()
                carryOn = False

            # Aggiorno il numero della partita
            if refermatch < matchnum:
                refermatch = matchnum

                pygame.display.flip()
                time.sleep(1)
                matchScreen(matchnum)

        except IndexError:
            pass

        # --- Disegno del gioco
        # Lo sfondo sarà nero
        screen.fill(BLACK)
        # La riga nel mezzo della finestra
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

        # Vengono disegnati tutti gli sprite allo stesso tempo
        all_sprites_list.draw(screen)

        # Il risultato
        font = pygame.font.Font("Data/coders_crux.ttf", 80)
        fontS = pygame.font.Font("Data/coders_crux.ttf", 40)
        text = font.render(str(scoreA), 1, WHITE)
        screen.blit(text, (250, 10))
        text = font.render(str(scoreB), 1, WHITE)
        screen.blit(text, (420, 10))

        text = fontS.render(str(subScoreA), 1, WHITE)
        screen.blit(text, (280, 60))
        text = fontS.render(str(subScoreB), 1, WHITE)
        screen.blit(text, (400, 60))
        # --- Lo schermo viene aggiornato
        pygame.display.flip()

        # --- 60 fps
        clock.tick(60)

    connection.serverDisconnect()


gameMenu()
