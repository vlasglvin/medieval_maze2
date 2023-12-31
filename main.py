from pygame import *
import os,sys
import random
import pickle


init()

font.init()
mixer.init()

from config import *
from HUD import Inventar, Counter, Label, MainMenu, PauseMenu, AboutMenu

tunnel_steps = mixer.Sound("assets/audio/steps in wood floor.wav")
grass_steps = mixer.Sound("assets/audio/leaves01.ogg")
tunnel_steps.set_volume(1)
grass_steps.set_volume(0.5)
guy_dying = mixer.Sound("assets/dying_guy.ogg")
enemy_damaging_sound = mixer.Sound("assets/audio/ogre5.wav")
potion_sound = mixer.Sound("assets/audio/bottle.wav")
chest_sound = mixer.Sound("assets/audio/door.wav")
bow_sound = mixer.Sound("assets/qubodup-wobble2.wav")
chest_sound.set_volume(0.2)
coin_sound = mixer.Sound("assets/audio/coinsplash.ogg")
coin_sound.set_volume(0.3)
sword_unleash = mixer.Sound("assets/audio/sword.1.ogg")
sword_unleash.set_volume(0.1)


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
arrows = sprite.Group()
spikes = sprite.Group()

groups_list = [potions, enemys, walls, chests, gold_bars, swords, arrows, spikes]

arrow_img = image.load("assets/arrow.png")
rage_power_sign = image.load("assets/S_Sword16.png")
power_sign = image.load("assets/S_Sword21.png")
heart_image = image.load("assets/heart pixel art 254x254.png")
right_arrow_image = image.load("assets/map/arrowSign.png")
left_arrow_image = transform.flip(right_arrow_image,True,False)
spear_image = image.load("assets/map/W_Spear005.png")
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
knife_image = image.load("assets/map/W_Dagger006.png")
suriken_image = image.load("assets/map/W_Throw05.png")
spike_image = image.load("assets/map/spike.png")

player_images = {}

folders = ["player_down", "player_left", "player_right", "player_up"]
for folder in folders:
    player_images[folder] = {
        "walking": get_image_list(folder + os.sep + "walking", 50, 50),
        "bow": get_image_list(folder + os.sep + "bow", 50, 50),
        "knife": get_image_list(folder + os.sep + "knife", 50, 50),
        "spear": get_image_list(folder + os.sep + "spear", 50, 50),
    }

enemy_down_img = get_image_list("enemy" + os.sep + "down", 40, 40)
enemy_left_img = get_image_list("enemy" + os.sep + "left", 40, 40)
enemy_right_img = get_image_list("enemy" + os.sep + "right", 40, 40)
enemy_up_img = get_image_list("enemy" + os.sep + "up", 40, 40)
enemy_killing_img = get_image_list("enemy" + os.sep + "killing", 40, 40)
item_list = {
    "healing potion" : potion_image, "rage potion" : red_potion_image, "gold bar" : goldbar_image,#"sword" : sword_image,
    "bow" : bow_image, "knife" : knife_image,"spear" : spear_image,"speed potion" : orange_potion_image
}

chest_item_list = list(item_list.keys())

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
    def __init__(self, images, x,y,width,height,speed,hp):
        super().__init__("player",images['player_down']["walking"][0],x,y,width,height)
        self.images = images
        self.speed = speed
        self.hp = hp
        self.min_speed = 2
        self.power = 10
        self.gold = 0
        self.weapon = None
        self.hit_image = None
        self.down_img = images['player_down']["walking"]
        self.right_img = images['player_right']["walking"]
        self.left_img = images['player_left']["walking"]
        self.up_img = images['player_up']["walking"]
        self.dir = "down"
        self.state = "stop"
        self.frame = 0
        self.frame_max = 5
        self.image_k = 0
        self.collided = False
        self.boosted = False
        self.boosted_timer = None
        self.speed_boosted = False
        self.speed_boosted_timer = 0
        self.old_speed = speed
        self.step_sound = grass_steps
        


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
            hp_counter.update_value(round(self.hp))
            self.collided = True
            guy_dying.play()

    def check_collision(self):
        
        potion_list = sprite.spritecollide(self, potions, True, sprite.collide_mask)
        for potion in potion_list:
            inventar.add_item(potion.type)

        chest_list = sprite.spritecollide(self, chests, False, sprite.collide_mask)
        for chest in chest_list:
            if not chest.opened:
                chest.open()
    
        spike_list = sprite.spritecollide(self, spikes, False, sprite.collide_mask)
        if len(spike_list) > 0:
            self.got_hit(0.1)

        gold_list = sprite.spritecollide(self, gold_bars, True, sprite.collide_mask)
        for gold in gold_list:
            self.gold += 1
            gold_counter.update_value(self.gold)
            coin_sound.play()
        
        enemy_list = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(enemy_list) > 0 and not self.hit_image:
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
        if keys[K_d]:
            self.rect.x += self.speed
            self.dir = "right"
            self.state = "move"
        elif keys[K_a]:
            self.rect.x -= self.speed
            self.dir = "left"
            self.state = "move"
        elif keys[K_w]:
            self.rect.y -= self.speed
            self.dir = "up"
            self.state = "move"
        elif keys[K_s]:
            self.rect.y += self.speed
            self.dir = "down"
            self.state = "move"
        
        else:
            self.state = "stop"

        if self.state != "stop" and not self.hit_image:
            self.animate()
            if self.step_sound.get_num_channels() == 0:
                self.step_sound.play(loops=-1)
        else:
            self.step_sound.stop()
        
        if self.check_collision():
            self.rect.x,self.rect.y = old_pos

        if self.hit_image:
            self.hit_animate()

        if self.boosted:
            now = time.get_ticks()
            if now - self.boosted_timer > 10000:
                self.power_booster(-30)

        if self.speed_boosted:
            now = time.get_ticks()
            if now - self.speed_boosted_timer > 10000:
                self.speed_booster(-5)


        elif self.hp <= 50 and self.speed != self.min_speed:
            self.old_speed = self.speed
            self.speed = self.min_speed
        else:
            self.speed = self.old_speed


    def heal(self, amount = 50):
        self.hp += 50
        hp_counter.update_value(self.hp)


    def power_booster(self, amount = 30):
        self.power += amount
        if amount > 0:
            self.boosted = True
            self.boosted_timer = time.get_ticks()
            power_counter.update_image(rage_power_sign)
        else:
            self.boosted = False
            power_counter.update_image(power_sign)
        power_counter.update_value(self.power)
        
    def speed_booster(self, amount = 7):
        self.speed += amount
        if amount > 0:
            self.speed_boosted = True
            self.speed_boosted_timer = time.get_ticks()
        else:
            self.speed_boosted = False

    
    def use_item(self, item_name):
        if item_name == "healing potion":
            self.heal()
            potion_sound.play()
        
        if item_name == "speed potion":
            if not self.speed_boosted:
                self.speed_booster(5)
            potion_sound.play()
        
        if item_name == "rage potion":
            self.power_booster(30)
            potion_sound.play()

        if item_name == "bow":
            if self.weapon:
                inventar.add_item(self.weapon)
            self.weapon = "bow"
            bow_sound.play()
        

        if item_name == "knife":
            if self.weapon:
                inventar.add_item(self.weapon)
            self.weapon = "knife"
            sword_unleash.play()
        
        if item_name == "spear":
            if self.weapon:
                inventar.add_item(self.weapon)
            self.weapon = "spear"
            bow_sound.play()

    def hit(self):
        if self.weapon:
            self.hit_image = self.images['player_'+self.dir][self.weapon]
            self.frame = 0
            self.image_k = 0

    def hit_animate(self): 
        self.frame += 1
        if self.frame == self.frame_max:
            self.frame = 0
            self.image_k += 1
            if self.image_k >= len(self.hit_image):
                self.hit_image = None
                if self.weapon == "bow":
                    arrows.add(Arrow(self.rect, 5, self.dir))
            else:     
                self.image = self.hit_image[self.image_k]



class Chest(GameSprite):


    def __init__(self,x,y,width,height):
        super().__init__("chest", chest_image,x,y,width,height)
        self.open_image = transform.scale(open_chest_image, (width, height))
        self.time = time.get_ticks()
        self.opened = False
        self.item = None

    def open(self):
        
        rand_item = random.choice(chest_item_list)
        self.item = rand_item
        self.opened = True
        self.image = self.open_image
        chest_sound.play()
        if self.item == "gold bar":
            player.gold += 1
            gold_counter.update_value(player.gold)
        else:  
            inventar.add_item(self.item)
            if self.item in weapon_list:
                chest_item_list.remove(self.item)
        self.time = time.get_ticks()
        return self.item
    
    def update(self):
        if self.opened and self.item:
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
        self.killing_img = enemy_killing_img
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
            if self.image_k >= len(self.down_img) and self.dir != "dead":
                self.image_k = 0
            if self.dir=="dead" and self.image_k >= len(self.killing_img):
                self.kill()
                return
            if self.dir == "down":
                self.image = self.down_img[self.image_k]
            elif self.dir == "up":
                self.image = self.up_img[self.image_k]
            elif self.dir == "left":
                self.image = self.left_img[self.image_k]
            elif self.dir == "right":
                self.image = self.right_img[self.image_k]
            else:
                self.image = self.killing_img[self.image_k]
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
        
        self.check_collision(player)
        self.animate()

    def check_collision(self, player):
        if sprite.collide_mask(self, player) and player.hit_image and player.weapon != "bow":
            self.hp -= player.power
            if self.hp <= 0:
                self.dir = "dead"
                self.image_k = 0
                self.frame_max  = 5
                self.frame = 0

        collide_list = sprite.spritecollide(self, arrows, True,)
        for arrow in collide_list:
            self.hp -= player.power
            if self.hp <= 0:
                self.dir = "dead"
                self.image_k = 0
                self.frame_max  = 5
                self.frame = 0
            
class Arrow(GameSprite):
    def __init__(self,rect,speed,dir):
        super().__init__("arrow",arrow_img,rect.x,rect.y,30,30)
        self.speed = 8
        self.dir = dir
        if self.dir == "up":
            self.image = transform.rotate(self.image, 90)
            self.rect.centerx = rect.centerx
            self.rect.bottom = rect.top
        elif self.dir == "down":
            self.image = transform.rotate(self.image, -90)
            self.rect.centerx = rect.centerx
            self.rect.top = rect.bottom
        elif self.dir == "left":
            self.image = transform.flip(self.image, False, True)
            self.rect.right = rect.left
            self.rect.centery = rect.centery
        else:
            self.rect.left = rect.right
            self.rect.centery = rect.centery
    def update(self):
        if self.dir == "up":
            self.rect.y -= self.speed
        elif self.dir == "down":
            self.rect.y += self.speed
        elif self.dir == "right":
            self.rect.x += self.speed
        elif self.dir == "left":
            self.rect.x -= self.speed
        collide_list = sprite.spritecollide(self, walls, False)
        if len(collide_list) > 0:
            self.kill()


window = display.set_mode((WIDTH,HEIGHT))
window_rect = Rect(0, 0, WIDTH, HEIGHT)
display.set_caption("Medieval Game")
clock  = time.Clock()




level = "level_1.txt"

class GameController:
    def __init__(self, level=1):
        self.level = level
        self.running = True
        self.pause = True
        self.game_over = False
        self.result = Label("GAME OVER", WIDTH/2, HEIGHT/2, 100, RED)
        self.menu = MainMenu(WIDTH, HEIGHT, self)
        self.pause_menu = PauseMenu(WIDTH/3, HEIGHT/3, self)
        self.about_menu = AboutMenu(WIDTH, HEIGHT, self)
        self.show_menu()
        #self.read_map()

    
    def show_menu(self):
        mixer.stop()
        mixer.music.load("assets/audio/Woodland Fantasy.mp3")
        mixer_music.set_volume(0.2)
        mixer.music.play()
        self.run_menu()

    def new_game(self):
        global player, inventar, hp_counter, gold_counter, power_counter
        for item in sprites:
                item.kill()
        player  = Player(player_images, 100, 100, 50, 50, 4 ,100)
        inventar = Inventar()
        hp_counter = Counter(player.hp, heart_image, 35,35,WIDTH - 150,HEIGHT - 40)
        gold_counter = Counter(player.gold, goldbar_image, 35,35,WIDTH - 270,HEIGHT - 40)
        power_counter = Counter(player.power, power_sign, 35,35, WIDTH - 380, HEIGHT - 40)
        self.level_counter = Label(self.level, 20, HEIGHT - 40)
        
        self.level = 1
        self.read_map()
        self.start_game()

    def start_game(self):
        mixer.stop()
        global BG_COLOR
        if self.level == 4:
            BG_COLOR = (34, 36, 34)
            mixer.music.load("assets/Overture.ogg")
            player.step_sound = tunnel_steps

        else:
            BG_COLOR = (129, 161, 0)
            mixer.music.load("assets/audio/Loop_Minstrel_Dance.wav")
        mixer_music.set_volume(0.2)
        mixer.music.play()
        self.level_counter = Label(f"Level: {self.level}", 70, HEIGHT - 25, 35)
        self.game_over = False
        self.running = True
        self.pause = False
        self.run()
        
    def save_game(self):
        if not self.game_over:
            with open("save.dat", "wb") as file:
                pickle.dump(self.level, file)
                pickle.dump(player.rect.x, file)
                pickle.dump(player.rect.y, file)
                pickle.dump(player.speed, file)
                pickle.dump(player.power, file)
                pickle.dump(player.gold, file)
                pickle.dump(player.hp, file)
                pickle.dump(player.weapon, file)
                pickle.dump(player.dir, file)
                pickle.dump(inventar.items, file)

                pickle.dump(len(enemys), file)
                for enemy in enemys:
                    pickle.dump(enemy.hp, file)
                    pickle.dump(enemy.dir, file)
                    pickle.dump(enemy.rect.centerx, file)
                    pickle.dump(enemy.rect.centery, file)

                pickle.dump(len(potions), file)
                for potion in potions:
                    pickle.dump(potion.type, file)
                    pickle.dump(potion.rect.centerx, file)
                    pickle.dump(potion.rect.centery, file)

                pickle.dump(len(gold_bars), file)
                for gold_bar in gold_bars:
                    pickle.dump(gold_bar.rect.centerx, file)
                    pickle.dump(gold_bar.rect.centery, file)
                
                pickle.dump(len(chests), file)
                for chest in chests:
                    pickle.dump(chest.rect.centerx, file)
                    pickle.dump(chest.rect.centery, file)
                    pickle.dump(chest.opened, file)
            
            self.resume()

    def load_map(self):
        global BG_COLOR

        with open(f"level_{self.level}.txt",'r', encoding="utf-8") as file:
            if self.level == 4:
                BG_COLOR = (34, 36, 34)
                mixer.music.load("assets/Overture.ogg")
                mixer.music.play()

            x, y = 25, 25
            map = file.readlines()
            for line in map:
                for symbol in line:
                    if symbol == "X":
                        walls.add(GameSprite("fence",fence_image , x,y, 50,25))

                    if symbol == "x":
                        walls.add(GameSprite("flip fence",left_fence_image , x,y, 25,50))

                    if symbol == "w":
                        walls.add(GameSprite("wall",wall_image , x,y, 50,50))

                    if symbol == "S":
                        new_spike = GameSprite("spike",spike_image , x,y, 35,35)
                        spikes.add(new_spike)
                        walls.add(new_spike)


                    if symbol == "A":
                        walls.add(GameSprite("arrow",right_arrow_image , x,y, 50,50))

                    if symbol == "a":
                        walls.add(GameSprite("arrow",left_arrow_image , x,y, 50,50))

                    x += 50

                x = 25
                y += 50

    def load_game(self):
        global player, inventar, hp_counter, gold_counter, power_counter
        
        for item in sprites:
                item.kill()
        
        player  = Player(player_images, 100, 100, 50, 50, 4 ,100)
        inventar = Inventar()
        
        if self.game_over:
            self.new_game()
            return
        try:
            with open("save.dat", "rb") as file:
                self.level = pickle.load(file)
                self.load_map()
                player.rect.x = pickle.load(file)
                player.rect.y = pickle.load(file)
                player.speed = pickle.load(file)
                player.power = pickle.load(file)
                player.gold = pickle.load(file)
                player.hp = pickle.load(file)
                player.weapon = pickle.load(file)
                player.dir = pickle.load(file)
                inventar.items = pickle.load(file)
            
                hp_counter = Counter(player.hp, heart_image, 35,35,WIDTH - 150,HEIGHT - 40)
                gold_counter = Counter(player.gold, goldbar_image, 35,35,WIDTH - 270,HEIGHT - 40)
                power_counter = Counter(player.power, power_sign, 35,35, WIDTH - 380, HEIGHT - 40)

                k_enemys = pickle.load(file)
                for i in range(k_enemys):
                    hp = pickle.load(file)
                    e_dir = pickle.load(file)
                    x = pickle.load(file)
                    y = pickle.load(file)
                    new_enemy = Enemy(x, y, 40,40,1 ,20)
                    new_enemy.dir = e_dir
                    enemys.add(new_enemy)

                k_potions = pickle.load(file)
                for i in range(k_potions):
                    potion_type = pickle.load(file)
                    x = pickle.load(file)
                    y = pickle.load(file)
                    if potion_type == "healing potion":
                        potions.add(GameSprite("healing potion",potion_image , x,y, 20,20))
                    if potion_type == "rage potion":
                            potions.add(GameSprite("rage potion",red_potion_image , x,y, 20,20))
                    if potion_type == "speed potion":
                            potions.add(GameSprite("speed potion",orange_potion_image , x,y, 20,20))

                k_gold_bars = pickle.load(file)
                for i in range(k_gold_bars):
                    x = pickle.load(file)
                    y = pickle.load(file)
                    gold_bars.add(GameSprite("gold bar",goldbar_image , x,y, 30,30))

                k_chests = pickle.load(file)
                for i in range(k_chests):
                    x = pickle.load(file)
                    y = pickle.load(file)
                    opened = pickle.load(file)
                    chest = Chest(x,y, 30,30,)
                    chest.opened = opened
                    if chest.opened:
                        chest.image = chest.open_image
                        
                    chests.add(chest)


            self.start_game()
        except OSError as e:
            self.new_game()
    
    def run_menu(self):
        
        while self.running:
            for e in event.get():
                if e.type == QUIT:
                    self.exit()

                if e.type == MOUSEBUTTONDOWN:
                    x, y = e.pos
                    click = self.menu.check_click(x, y)
                    if click:
                        quit()
            
            self.menu.draw(window)
            display.update()
            clock.tick(FPS)

    def run_about_menu(self):
         
        while self.running:
            for e in event.get():
                if e.type == QUIT:
                    self.exit()

                if e.type == MOUSEBUTTONDOWN:
                    x, y = e.pos
                    click = self.about_menu.check_click(x, y)
                    if click:
                        quit()
                        
            
            self.about_menu.draw(window)
            display.update()
            clock.tick(FPS)



    def read_map(self):
        global BG_COLOR
        if self.level == 4:
            BG_COLOR = (34, 36, 34)
            mixer.music.load("assets/Overture.ogg")
            player.step_sound.stop()
            player.step_sound = tunnel_steps
            mixer.music.play()
        with open(f"level_{self.level}.txt",'r', encoding="utf-8") as file:
            
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

                    if symbol == "S":
                        new_spike = GameSprite("spike",spike_image , x,y, 35,35)
                        spikes.add(new_spike)
                        walls.add(new_spike)

                    if symbol == "C":
                        chests.add(Chest(x,y, 30,30,))

                    if symbol == "R":
                        potions.add(GameSprite("rage potion",red_potion_image , x,y, 20,20))

                    if symbol == "O":
                        potions.add(GameSprite("speed potion",orange_potion_image , x,y, 20,20))

                    if symbol == "G":
                        gold_bars.add(GameSprite("gold bar",goldbar_image , x,y, 30,30))

                    # if symbol == "S":
                    #     swords.add(GameSprite("sword",sword_image , x,y, 30,30))

                    if symbol == "A":
                        walls.add(GameSprite("arrow",right_arrow_image , x,y, 50,50))

                    if symbol == "a":
                        walls.add(GameSprite("arrow",left_arrow_image , x,y, 50,50))

                    x += 50

                x = 25
                y += 50
    
    def events(self):
        for e in event.get():
            if e.type == QUIT:
                self.exit()
            if e.type == KEYDOWN:
                if e.key == K_e:
                    if not inventar.is_open == True and not self.pause:
                        inventar.is_open = True
                    else:
                        inventar.is_open = False
        
                if e.key == K_f:
                    player.hit()

                if e.key == K_ESCAPE:
                    if self.game_over:
                        self.show_menu()
                    self.pause = not self.pause

            if e.type == MOUSEBUTTONDOWN and self.pause:
                x, y = e.pos
                self.pause_menu.check_click(x,y)

            
            if e.type == MOUSEBUTTONDOWN and inventar.is_open:
                x, y = e.pos
                selected_item = inventar.select(x, y)
                
                if selected_item:
                    player.use_item(selected_item)

            

    def update(self):
        if player.hp <= 0:
            self.result.set_text("GAME OVER")
            self.game_over = True
        sprites.update()
        inventar.update()

    def draw(self):
        
        if player.hp <= 0:
            self.game_over = True
        
        window.fill(BG_COLOR)
        sprites.draw(window)
        inventar.draw(window, item_list)
        hp_counter.draw(window)
        gold_counter.draw(window)
        power_counter.draw(window)
        self.level_counter.draw(window)

        if self.game_over:
            self.result.draw(window)
        
        if self.pause:
                self.pause_menu.draw(window)


    def next_level(self):
        global player    
        self.level += 1
        self.level_counter.set_text(f"Level: {self.level}")
        if self.level > MAX_LEVEL:
            self.level = MAX_LEVEL
            return 0
        for gamesprite in sprites:
            if gamesprite.type != "player":
                gamesprite.kill()
        #player  = Player(player_images, 100, 100, 50, 50, 4 ,100)
        self.read_map()
        return self.level

    def resume(self):
        self.pause = False
    
    
    
    def run(self):
        while self.running:
            self.events()
            self.draw()
            if not self.game_over and not self.pause:
                self.update()
            if not player.rect.colliderect(window_rect):
                if not self.next_level() and not self.game_over:
                    self.result.set_text("YOU WIN")
                    self.game_over = True

                
            display.update()
            clock.tick(FPS)
           
    def exit(self):
        self.running = False
        sys.exit()

game = GameController()
#game.run()