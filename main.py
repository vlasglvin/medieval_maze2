from pygame import *
init()
WIDTH,HEIGHT = 1000,700
FPS = 60


class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image,x,y,width,height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width,height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.mask = mask.from_surface(self.image)
    
    def draw(self,window):
        window.blit(self.image,self.rect)

class Player(GameSprite):
    def __init__(self,sprite_image,x,y,width,height,speed,hp):
        super().__init__(sprite_image,x,y,width,height)
        self.speed = speed
        self.hp = hp


window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Medieval Game")
clock  = time.Clock()
run = True

player  = Player("assets/frame_00_delay-0.12s.png",100,100,65,65,5,3)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    player.draw(window)

    display.update()
    clock.tick(FPS)

