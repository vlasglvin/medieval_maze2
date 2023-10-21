from pygame import *
font.init()

INV_WIDTH, INV_HEIGHT = 300,300
ITEM_WIDTH, ITEM_HEIGHT = INV_WIDTH/4, INV_HEIGHT/4

class Inventar(sprite.Sprite):
    def __init__(self):
        self.items = {}
        self.items_images = []
        self.surface = Surface((INV_WIDTH, INV_HEIGHT))
        self.image = transform.scale(image.load("assets/inventory_slots.jpg"), (INV_WIDTH, INV_HEIGHT))
        self.is_open = False
        self.font = font.Font("assets/alagard_by_pix3m-d6awiwp.ttf", 35)
    
    def add_item(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            if len(self.items) < 16:
                self.items[item] = 1
    
    def draw(self, window, item_list):
        if self.is_open:
            self.surface.blit(self.image, (0,0))
            x, y = 0, 0
            for item in self.items:
                img = transform.scale(item_list[item], (ITEM_WIDTH, ITEM_HEIGHT))
                self.surface.blit(img, (x,y))
                k = str(self.items[item])
                self.surface.blit(self.font.render(k, True,(255, 255, 255)), (x+10,y+10))
                x += ITEM_WIDTH
                if x >= INV_HEIGHT:
                    y += ITEM_HEIGHT
                    x = 0
            window.blit(self.surface, (0,500))
