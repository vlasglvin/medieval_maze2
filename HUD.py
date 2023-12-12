from pygame import *
font.init()

from config import *

menu_bg = image.load("assets/shadowed_bg.png")
menu_btn = image.load("assets/menu_button.png")

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
        if item in self.items:
            
            self.items[item] += 1
            if item in weapon_list:
                self.items[item] = 1
        else:
            if len(self.items) < 16:
                self.items[item] = 1
    
    def remove_item(self, item):
        if item in self.items:
            self.items[item] -= 1
        if self.items[item]==0:
            self.items.pop(item)
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
        self.label = self.font.render(str(round(value)), True, (255, 255, 255))
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

class Button(sprite.Sprite):
    def __init__(self, text, action, x, y, width=298, height=71, font_size = 30):
        super().__init__()
        self.font = font.Font(FONT_PATH, font_size)
        self.image = transform.scale(menu_btn, (width, height))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x,y
        self.label = self.font.render(str(text), True, (32, 34, 36))
        self.label_rect = self.label.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.width, self.height = width, height
        self.action = action

    def draw(self, window):
        window.blit(self.image, self.rect)
        window.blit(self.label, self.label_rect)

    

class MainMenu(Surface):
    def __init__(self, width, height, game):
        super().__init__((width, height), SRCALPHA, 32)
        self.game = game
        self.image = transform.scale(menu_bg.convert_alpha(), (width, height))
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.bg_color = (43, 30, 30)
        self.width = width
        self.height = height
        self.main_text = Label("Medieval Maze", WIDTH/2, 150, 100, (133, 77, 32))
        self.options = [Button("Play", self.game.load_game, WIDTH/2, 250, width=400, height=93, font_size = 50),
                        Button("New Game", self.game.new_game, WIDTH/2, 360),
                        Button("About", quit, WIDTH/2, 460),
                        Button("Exit", quit, WIDTH/2, 560)]

    def draw(self, window):
        self.fill(self.bg_color)
        self.blit(self.image, (0,0))
        window.blit(self, self.rect)
        self.main_text.draw(window)
        for btn in self.options:
            btn.draw(window)
       
    def check_click(self, x, y):
        for btn in self.options:
            if btn.rect.collidepoint(x, y):
                btn.action()
                return True
        return False
    
class PauseMenu(MainMenu):
    def __init__(self, width, height, game):
        super().__init__(width, height, game)
        self.image = transform.scale(menu_bg.convert_alpha(), (width, height))
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.options = [Button("Resume", self.game.resume, WIDTH/2, 360, width=250, height=60, font_size= 25),
                        Button("Save Game", self.game.save_game, WIDTH/2, 410,  width=250, height=60, font_size= 25),
                        Button("Main Menu", self.game.show_menu, WIDTH/2, 460,  width=250, height=60, font_size= 25)]
        
    def draw(self, window):
        window.blit(self.image, self.rect)
        for btn in self.options:
            btn.draw(window)