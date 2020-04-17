import pygame
from random import randint

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        # Chiama il costruttore della classe Sprite
        super().__init__()

        # Vengono passati il colore, la larghezza e l'altezza della palla
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.width = width
        self.height = height

        # Viene disegnata la palla
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4, 8), randint(-8, 8)]

        # Viene "preso" un rettangolo che ha le dimensioni dell'immagine
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)

    def getSize(self):
        return ";".join([str(self.width), str(self.height)])
