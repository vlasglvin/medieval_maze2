from pygame import *
import os
import random

from HUD import Inventar, Counter

init()

font.init()
mixer.init()
mixer.music.load("assets/audio/Loop_Minstrel_Dance.wav")
mixer_music.set_volume(0.2)
mixer.music.play()
enemy_damaging_sound = mixer.Sound("assets/audio/ogre5.wav")
potion_sound = mixer.Sound("assets/audio/bottle.wav")
chest_sound = mixer.Sound("assets/audio/door.wav")
chest_sound.set_volume(0.2)
coin_sound = mixer.Sound("assets/audio/coinsplash.ogg")
coin_sound.set_volume(0.3)
sword_unleash = mixer.Sound("assets/audio/sword.1.ogg")
sword_unleash.set_volume(0.1)
WIDTH,HEIGHT = 1400,830
FPS = 60
BG_COLOR = (129, 161, 0)
PATH = os.getcwd()

ASSETS_PATH = os.path.join(PATH, "assets")#game adress

def get_image_list(foldername, width, height):
    path_dir = os.path.join(ASSETS_PATH, foldername)#assets folder adress
    image_names = os.listdir(path_dir)#player down adress
    image_list = []

    for img in image_names:
        new_image = image.load(os.path.join(path_dir, img))
        resize_image = transform.scale(new_image, (width, height))
        image_list.append(resize_image)


    return image_list

potions = sprite.Group()
sprites = sprite.Group()
enemys = sprite.Group()
walls = sprite.Group()
chests = sprite.Group()
gold_bars = sprite.Group()
swords = sprite.Group()

heart_image = image.load("assets/heart pixel art 254x254.png")
right_arrow_image = image.load("assets/map/arrowSign.png")
left_arrow_image = transform.flip(right_arrow_image,True,False)
sword_image = image.load("assets/map/S_Sword09.png")
goldbar_image = image.load("assets/map/I_GoldBar.png")
player_image = image.load("assets/frame_00_delay-0.12s.png")
fence_image = image.load("assets/map/fence.png")
left_fence_image = transform.rotate(fence_image, 90)
wall_image = image.load("assets/map/wall.png")
skeleton_image = image.load("assets/enemy/skeleton.png")
red_potion_image = image.load("assets/map/P_Red01.png")
potion_image = image.load("assets/map/P_Medicine04.png")
chest_image = image.load("assets/map/I_Chest01.png")
open_chest_image = image.load("assets/map/I_Chest02.png")
bow_image = image.load("assets/map/W_Bow02.png")
axe_image = image.load("assets/map/W_Axe009.png")
orange_potion_image = image.load("assets/map/P_Orange02.png")
dagger_image = image.load("assets/map/W_Dagger006.png")
suriken_image = image.load("assets/map/W_Throw05.png")
spike_image = image.load("assets/map/spike.png")

player_down_img = get_image_list("player_down" + os.sep + "walking", 50, 50)
player_left_img = get_image_list("player_left" + os.sep + "walking", 50, 50)
player_right_img = get_image_list("player_right" + os.sep + "walking", 50, 50)
player_up_img = get_image_list("player_up" + os.sep + "walking", 50, 50)\

enemy_down_img = get_image_list("enemy" + os.sep + "down", 50, 50)
enemy_left_img = get_image_list("enemy" + os.sep + "left", 50, 50)
enemy_right_img = get_image_list("enemy" + os.sep + "right", 50, 50)
enemy_up_img = get_image_list("enemy" + os.sep + "up", 50, 50)
item_list = {
    "healing potion" : potion_image, "rage potion" : red_potion_image, "gold bar" : goldbar_image,"sword" : sword_image,
    "bow" : bow_image, "dagger" : dagger_image, "suriken" : suriken_image, "axe" : axe_image,
      "speed potion" : orange_potion_image
}


class GameSprite(sprite.Sprite):
    def __init__(self,type,sprite_image,x,y,width,height):
        super().__init__()
        self.type = type
        self.width = width
        self.height = height
        self.image = transform.scale(sprite_image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)
    
    def draw(self,window):
        window.blit(self.image,self.rect)

    def update(self):
        pass

class Player(GameSprite):
    def __init__(self,x,y,width,height,speed,hp):
        super().__init__("player",player_down_img[0],x,y,width,height)
        self.speed = speed
        self.hp = hp
        self.gold = 0
        self.weapon = ""
        self.down_img = player_down_img
        self.right_img = player_right_img
        self.left_img = player_left_img
        self.up_img = player_up_img
        self.dir = "down"
        self.frame = 0
        self.frame_max = 5
        self.image_k = 0
        self.collided = False

    def animate(self):
        self.frame += 1
        if self.frame == self.frame_max:
            self.frame = 0
            self.image_k += 1
            if self.image_k >= len(self.down_img):
                self.image_k = 0
            if self.dir == "down":
                self.image = self.down_img[self.image_k]
            elif self.dir == "up":
                self.image = self.up_img[self.image_k]
            elif self.dir == "left":
                self.image = self.left_img[self.image_k]
            elif self.dir == "right":
                self.image = self.right_img[self.image_k]

    def got_hit(self, damage = 10):
        if  not self.collided == True:
            self.hp -= damage
            hp_counter.update_value(self.hp)
            self.collided = True

    def check_collision(self):
        
        potion_list = sprite.spritecollide(self, potions, True, sprite.collide_mask)
        for potion in potion_list:
            inventar.add_item(potion.type)

        chest_list = sprite.spritecollide(self, chests, False, sprite.collide_mask)
        for chest in chest_list:
            if not chest.opened:
                chest.open()
    
        sword_list = sprite.spritecollide(self, swords, True, sprite.collide_mask)
        for sword in sword_list:
            self.weapon = "sword"
            sword_unleash.play()
        
        gold_list = sprite.spritecollide(self, gold_bars, True, sprite.collide_mask)
        for gold in gold_list:
            self.gold += 1
            gold_counter.update_value(self.gold)
            coin_sound.play()
        
        enemy_list = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(enemy_list) > 0:
            self.got_hit()
        else:
            self.collided = False
        
            
        if len(enemy_list) == 0:
            self.collided = False

        collide_list = sprite.spritecollide(self, walls, False,sprite.collide_mask)
        if len(collide_list)> 0:
            return True
        else:
            return False

    def update(self):
        '''
        movement control from keyboard
        '''                
        keys = key.get_pressed()
        old_pos =  self.rect.x,self.rect.y
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.dir = "right"
        elif keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.dir = "left"
        elif keys[K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.dir = "up"
        elif keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.dir = "down"
        
        else:
            self.dir = "stop"

        if self.dir != "stop":
            self.animate()
        
        if self.check_collision():
            self.rect.x,self.rect.y = old_pos
    def heal(self, amount = 50):
        self.hp += 50
        hp_counter.update_value(self.hp)

    
    def use_item(self, item_name):
        if item_name == "healing potion":
            self.heal()
            potion_sound.play()

class Chest(GameSprite):


    def __init__(self,x,y,width,height):
        super().__init__("chest", chest_image,x,y,width,height)
        self.open_image = transform.scale(open_chest_image, (width, height))
        rand_item = random.choice(list(item_list.keys()))
        self.time = time.get_ticks()
        self.item = rand_item
        self.opened = False
        print(self.item)
    
    def open(self):
        
        self.opened = True
        self.image = self.open_image
        chest_sound.play()
        inventar.add_item(self.item)
        self.time = time.get_ticks()
        return self.item
    
    def update(self):
        if self.opened == True:
            if time.get_ticks() - self.time < 1000:
                window.blit(item_list[self.item], (self.rect.x + -25,self.rect.top - 5))

class Enemy(GameSprite):
    def __init__(self,x,y,width,height,speed,hp):
        super().__init__("enemy",enemy_down_img[0],x,y,width,height)
        self.speed = speed
        self.hp = hp
        self.down_img = enemy_down_img
        self.right_img = enemy_right_img
        self.left_img = enemy_left_img
        self.up_img = enemy_up_img
        self.dir = "down"
        self.dir_list = ["down", "up", "right", "left"]
        self.frame = 0
        self.frame_max = 10
        self.image_k = 0

    def animate(self):
        self.frame += 1
        if self.frame == self.frame_max:
            self.frame = 0
            self.image_k += 1
            if self.image_k >= len(self.down_img):
                self.image_k = 0
            if self.dir == "down":
                self.image = self.down_img[self.image_k]
            elif self.dir == "up":
                self.image = self.up_img[self.image_k]
            elif self.dir == "left":
                self.image = self.left_img[self.image_k]
            elif self.dir == "right":
                self.image = self.right_img[self.image_k]
            self.mask = mask.from_surface(self.image)

    def update(self):
        old_pos =  self.rect.x,self.rect.y
        if self.dir == "down":
            self.rect.y += self.speed
        if self.dir == "up":
            self.rect.y -= self.speed
        if self.dir == "right":
            self.rect.x += self.speed
        if self.dir == "left":
            self.rect.x -= self.speed
        
        collide_list = sprite.spritecollide(self, walls, False,)
        if len(collide_list) > 0 or  not window_rect.contains(self.rect):
            self.rect.x,self.rect.y = old_pos
            list_dir = self.dir_list.copy()  
            list_dir.remove(self.dir)
            self.dir = random.choice(list_dir)
   
        self.animate()

window = display.set_mode((WIDTH,HEIGHT))
window_rect = Rect(0, 0, WIDTH, HEIGHT)
display.set_caption("Medieval Game")
clock  = time.Clock()
run = True

player  = Player(100, 100, 50, 50, 4 ,100)
inventar = Inventar()
hp_counter = Counter(player.hp, heart_image, 35,35,WIDTH - 150,HEIGHT - 40)
gold_counter = Counter(player.gold, goldbar_image, 35,35,WIDTH - 270,HEIGHT - 40)

with open("level_2.txt",'r', encoding="utf-8") as file:
    x, y = 25, 25
    map = file.readlines()
    for line in map:
        for symbol in line:
            if symbol == "X":
                walls.add(GameSprite("fence",fence_image , x,y, 50,25))
            
            if symbol == "P":
                player.rect.x = x
                player.rect.y = y
            
            if symbol == "E":
                enemys.add(Enemy(x,y, 40,40,1 ,20))

            if symbol == "H":
                potions.add(GameSprite("healing potion",potion_image , x,y, 20,20))

            if symbol == "x":
                walls.add(GameSprite("flip fence",left_fence_image , x,y, 25,50))

            if symbol == "w":
                walls.add(GameSprite("wall",wall_image , x,y, 50,50))

            if symbol == "C":
                chests.add(Chest(x,y, 30,30,))

            if symbol == "R":
                potions.add(GameSprite("rage potion",red_potion_image , x,y, 20,20))

            if symbol == "O":
                potions.add(GameSprite("speed potion",orange_potion_image , x,y, 20,20))

            if symbol == "G":
                gold_bars.add(GameSprite("gold bar",goldbar_image , x,y, 30,30))

            if symbol == "S":
                swords.add(GameSprite("sword",sword_image , x,y, 30,30))

            if symbol == "A":
                walls.add(GameSprite("arrow",right_arrow_image , x,y, 50,50))

            if symbol == "a":
                walls.add(GameSprite("arrow",left_arrow_image , x,y, 50,50))

            x += 50

        x = 25
        y += 50

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_e:
                if not inventar.is_open == True:
                    inventar.is_open = True
                else:
                    inventar.is_open = False
    
        if e.type == MOUSEBUTTONDOWN and inventar.is_open:
            x, y = e.pos
            selected_item = inventar.select(x, y)
            
            if selected_item:
                player.use_item(selected_item)

    window.fill(BG_COLOR)
    sprites.draw(window)
    sprites.update()
    inventar.draw(window, item_list)
    inventar.update()
    hp_counter.draw(window)
    gold_counter.draw(window)
    display.update()
    clock.tick(FPS)