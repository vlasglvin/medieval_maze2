from pygame import *

init()

font.init()
mixer.init()
mixer.music.load("assets/audio/Loop_Minstrel_Dance.wav")
mixer_music.set_volume(0.2)
mixer.music.play()
coin_sound = mixer.Sound("assets/audio/coinsplash.ogg")
sword_unleash = mixer.Sound("assets/audio/sword.1.ogg")

WIDTH,HEIGHT = 1400,800
FPS = 60
BG_COLOR = (129, 161, 0)


potions = sprite.Group()
sprites = sprite.Group()
enemys = sprite.Group()
walls = sprite.Group()
chests = sprite.Group()
gold_bars = sprite.Group()
swords = sprite.Group()


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


class GameSprite(sprite.Sprite):
    def __init__(self,type,sprite_image,x,y,width,height):
        super().__init__()
        self.type = type
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
    def __init__(self,sprite_image,x,y,width,height,speed,hp):
        super().__init__("player",sprite_image,x,y,width,height)
        self.speed = speed
        self.hp = hp
        self.gold = 0
        self.weapon = ""


    def check_collision(self):
        
        sword_list = sprite.spritecollide(self, swords, True, sprite.collide_mask)
        for sword in sword_list:
            self.weapon = "sword"
            sword_unleash.play()
        
        
        gold_list = sprite.spritecollide(self, gold_bars, True, sprite.collide_mask)
        for gold in gold_list:
            self.gold += 1
            coin_sound.play()
        
 
        
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
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

        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[K_w] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

        if old_pos[0] != self.rect.x or old_pos[1] != self.rect.y:
            if self.check_collision():
                self.rect.x,self.rect.y = old_pos



window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Medieval Game")
clock  = time.Clock()
run = True

player  = Player(player_image,100, 100, 50, 50, 4 ,3)

with open("level_1.txt",'r', encoding="utf-8") as file:
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
                enemys.add(GameSprite("enemy",skeleton_image , x,y, 35,40))

            if symbol == "H":
                potions.add(GameSprite("healing potion",potion_image , x,y, 20,20))

            if symbol == "x":
                walls.add(GameSprite("flip fence",left_fence_image , x,y, 25,50))

            if symbol == "w":
                walls.add(GameSprite("wall",wall_image , x,y, 50,50))

            if symbol == "C":
                chests.add(GameSprite("chest",chest_image , x,y, 30,30))

            if symbol == "R":
                potions.add(GameSprite("rage potion",red_potion_image , x,y, 20,20))

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
    window.fill(BG_COLOR)
    sprites.draw(window)
    sprites.update()

    display.update()
    clock.tick(FPS)

