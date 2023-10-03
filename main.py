from pygame import *

init()
WIDTH,HEIGHT = 1000,700
FPS = 60
BG_COLOR = (129, 161, 0)

potions = sprite.Group()
sprites = sprite.Group()
enemys = sprite.Group()
walls = sprite.Group()
chests = sprite.Group()

player_image = image.load("assets/frame_00_delay-0.12s.png")
fence_image = image.load("assets/map/fence.png")
left_fence_image = transform.rotate(fence_image, 90)
wall_image = image.load("assets/map/wall.png")
skeleton_image = image.load("assets/enemy/skeleton.png")
potion_image = image.load("assets/map/P_Medicine04.png")
chest_image = image.load("assets/map/I_Chest01.png")


class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image,x,y,width,height):
        super().__init__()
        self.image = transform.scale(sprite_image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)
    
    def draw(self,window):
        window.blit(self.image,self.rect)

    def update(self):
        pass

class Player(GameSprite):
    def __init__(self,sprite_image,x,y,width,height,speed,hp):
        super().__init__(sprite_image,x,y,width,height)
        self.speed = speed
        self.hp = hp

    def update(self):
        '''
        movement control from keyboard
        '''                
        keys = key.get_pressed()

        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[K_w] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Medieval Game")
clock  = time.Clock()
run = True

player  = Player(player_image,100, 100, 65, 65, 5 ,3)

with open("level_1.txt",'r', encoding="utf-8") as file:
    x, y = 0, 10
    map = file.readlines()
    for line in map:
        for symbol in line:
            if symbol == "X":
                walls.add(GameSprite(fence_image , x,y, 50,25))
            
            if symbol == "P":
                player.rect.x = x
                player.rect.y = y
            
            if symbol == "E":
                enemys.add(GameSprite(skeleton_image , x,y, 50,50))

            if symbol == "H":
                potions.add(GameSprite(potion_image , x,y, 15,15))

            if symbol == "x":
                walls.add(GameSprite(left_fence_image , x,y, 25,50))

            if symbol == "w":
                walls.add(GameSprite(wall_image , x,y, 50,50))

            if symbol == "C":
                chests.add(GameSprite(chest_image , x,y, 25,25))
            x += 50

        x = 0
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

