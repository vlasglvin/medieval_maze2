from pygame import *
font.init()

INV_WIDTH, INV_HEIGHT = 300,300
ITEM_WIDTH, ITEM_HEIGHT = INV_WIDTH/4, INV_HEIGHT/4
FONT_PATH = "assets/alagard_by_pix3m-d6awiwp.ttf"

weapon_list = ["bow", "knife", "spear"]
menu_bg = image.load("assets/parchment_alpha.png")

class Inventar(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.items = {}
        self.items_images = []
        self.surface = Surface((INV_WIDTH, INV_HEIGHT))
        self.image = transform.scale(image.load("assets/inventory_slots.jpg"), (INV_WIDTH, INV_HEIGHT))
        self.is_open = False
        self.font = font.Font(FONT_PATH, 35)
    
    def add_item(self, item):
        if item in self.items and not item in weapon_list:
            self.items[item] += 1
        else:
            if len(self.items) < 16:
                self.items[item] = 1
    
    def remove_item(self, item):
        if item in self.items:
            self.items[item] -= 1
        if self.items[item]==0:
            del self.items[item]
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

    def select(self, x, y):
        if self.is_open == True:
            if x > 0 and x < 300 and y > 500 and y < 500 + INV_HEIGHT:
                item_x, item_y = 0, 500
                item_number = 0
                for row in range(4):
                    for col in range(4):
                        item_rect = Rect(item_x, item_y, ITEM_WIDTH, ITEM_HEIGHT)
                        if item_rect.collidepoint(x, y) and item_number < len(self.items):
                            item = list(self.items.keys())[item_number]
                            self.remove_item(item)
                            return item
                        item_number += 1
                        item_x += ITEM_WIDTH
                    item_y += ITEM_HEIGHT
class Counter():
    def __init__ (self,value, image, width, height, x, y):
        self.font = font.Font(FONT_PATH, height)
        self.image = transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.label = self.font.render(str(value), True, (255, 255, 255))
        self.width, self.height = width, height

    def draw(self, window):
        window.blit(self.image, self.rect)
        window.blit(self.label, (self.rect.right + 15, self.rect.y))

    def update_value(self, new_value):
        self.label = self.font.render(str(round(new_value)), True, (255, 255, 255))

    def update_image(self, new_image):
        self.image = transform.scale(new_image, (self.width, self.height))

class Label:
    def __init__(self, text, x ,y,font_size = 30, color = (255, 255, 255)):
        self.font = font.Font(FONT_PATH, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y
        self.color = color

    def draw(self, window):
        window.blit(self.image, self.rect)
    
    def set_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)


class MainMenu(Surface):
    def __init__(self, width, height):
        super().__init__((width, height))
        self.image = transform.scale(menu_bg, (width, height))
        self.bg_color = (129, 161, 0)
        self.width = width
        self.height = height

    def draw(self, window):
        self.fill(self.bg_color)
        self.blit(self.image, (0,0))
        window.blit(self, (0,0))
