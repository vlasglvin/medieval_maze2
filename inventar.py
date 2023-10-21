from pygame import *

INV_WIDTH, INV_HEIGHT = 300,300
ITEM_WIDTH, ITEM_HEIGHT = INV_WIDTH/4, INV_HEIGHT/4

class Inventar(sprite.Sprite):
    def __init__(self):
        self.items = {}
        self.items_images = []
        self.surface = Surface((INV_WIDTH, INV_HEIGHT))
        self.image = transform.scale(image.load("assets/inventory_slots.jpg"), (INV_WIDTH, INV_HEIGHT))
        self.is_open = False
    
    def add_item(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1
        print(self.items)
    
    def draw(self, window, item_list):
        if self.is_open:
            self.surface.blit(self.image, (0,0))
            x, y = 0, 0
            for item in self.items:
                img = transform.scale(item_list[item], (ITEM_WIDTH, ITEM_HEIGHT))
                self.surface.blit(img, (x,y))
                x += ITEM_WIDTH
            window.blit(self.surface, (0,500))