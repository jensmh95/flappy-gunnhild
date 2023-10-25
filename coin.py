import pygame
import random

class Coin(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if type == "beer":
            beer_surf = pygame.transform.scale2x(
                pygame.image.load("sprites/beer.png")
            ).convert_alpha()
            self.frames = [beer_surf]
        else:
            shot_surf = pygame.transform.scale(
                pygame.image.load("sprites/tequila-shot-clipart-md.png"),(60,60)
            ).convert_alpha()
            self.frames = [shot_surf]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midtop=(700, random.randint(200, 700)))

    def update(self):
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()