from pygame import *

INV_WIDTH, INV_HEIGHT = 300,300

class Inventar(sprite.Sprite):
    def __init__(self):
        self.items = {}
        self.surface = Surface((INV_WIDTH, INV_HEIGHT))
        self.image = transform.scale(image.load("assets/inventory_slots.jpg"), (INV_WIDTH, INV_HEIGHT))
    def draw(self, window):
        self.surface.blit(self.image, (0,0))
        window.blit(self.surface, (0,500))
