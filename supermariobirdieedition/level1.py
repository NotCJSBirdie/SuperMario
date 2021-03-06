import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

window_width = 500
window_height = 500

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Birdie Platform')

#define tilesize
tilesize = 25
gameover = 0
mainmenu = True 

#load images
bg_picture = pygame.image.load("C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/bg.jpg")
restart = pygame.image.load("C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/reset.png")
start =  pygame.image.load("C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/start.png")
end = pygame.image.load("C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/exit.png")

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw(self):


        mouseaction = False
        #get mouse position

        position = pygame.mouse.get_pos()

        #check mouseover & clicked conditions

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                mouseaction = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
                
        #draw button
        window.blit(self.image, self.rect)

        return mouseaction


class Player():
    def __init__(self, x ,y):
        self.reset(x, y)

    def update(self, gameover):


        dx = 0
        dy = 0
        walkcooldown = 20

        if gameover == 0:

            #get key presses

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.inair == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False 
            if key[pygame.K_LEFT]:
                dx -= 1
                self.counter +=5
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 1
                self.counter +=5
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            

            #handle animation

            if self.counter >= walkcooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            





            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10

            dy += self.vel_y
            #collision

            self.inair = True

            for tile in world.tilelist:
                #check collison in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground , jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                #check if above the ground , falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.inair = False

            #check collision of enemies
            if pygame.sprite.spritecollide(self, goombagroup, False):
                gameover = -1

             #check collision of lava
            if pygame.sprite.spritecollide(self, lavagroup, False):
                gameover = -1
                        

            #update coordinates
            self.rect.x += dx
            self.rect.y += dy



        elif gameover == -1:
                self.image = self.deadimage
                if self.rect.y > 200:
                    self.rect.y -= 5

        #draw player onto the screen
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)


        return gameover

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f"C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (25, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.deadimage = pygame.image.load("C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/ghost.jpg")
        self.deadimage = pygame.transform.scale(self.deadimage, (25, 50))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width =self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.inair = True

class World():
    def __init__(self, data):

        self.tilelist = []

        #load images
        dirt_picture = pygame.image.load("C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/dirt.png")

        rowcount = 0
        for horizontalrow in data:
            columncount = 0 
            for tile in horizontalrow:
                if tile == 1:
                    img = pygame.transform.scale(dirt_picture, (tilesize, tilesize))
                    rectangle = img.get_rect()
                    rectangle.x = columncount * tilesize
                    rectangle.y = rowcount * tilesize
                    tile = (img, rectangle)
                    self.tilelist.append(tile)
                if tile == 3:
                    goomba = Enemy(columncount * tilesize, rowcount * tilesize)
                    goombagroup.add(goomba)
                if tile == 4:
                    lava = Lava(columncount * tilesize, rowcount * tilesize)
                    lavagroup.add(lava)
                columncount += 1
            rowcount += 1
    def draw(self):
        for tile in self.tilelist:
            window.blit(tile[0], tile[1])
            pygame.draw.rect(window, (255, 255, 255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/goomba1.png')
        self.image = pygame.transform.scale(self.image, (20,30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movedirection = 1
        self.movecounter = 0

    def update(self):

        self.rect.x += self.movedirection
        self.movecounter += 1
        if self.movecounter > 30:
            self.movedirection *= -1
            self.movecounter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('C:/Users/realcjsphotography/OneDrive/Desktop/platformerimages/lava.jpeg')
        self.image = pygame.transform.scale(img, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
       


dataofworld = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 4, 4, 4, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

restartbutton = Button(window_width // 2 - 50, window_height // 2 - 150, restart)
startbutton = Button(window_width // 2 - 100, window_height // 2 - 200, start)
exitbutton = Button(window_width // 2 - 20, window_height // 2 - 200, end)
player = Player(100, window_height - 80)
goombagroup = pygame.sprite.Group()
lavagroup = pygame.sprite.Group()
world = World(dataofworld)


gamerun = True
while gamerun:

    clock.tick(fps)
    
    window.blit(bg_picture, (0, 0))

    if mainmenu == True:
        
        if exitbutton.draw():
            gamerun = False
        if startbutton.draw():
            mainmenu = False

    else:

        world.draw()

        if gameover == 0:
            goombagroup.update()
            

        
        goombagroup.draw(window)
        lavagroup.draw(window)

        gameover = player.update(gameover)

        #if player has died
        if gameover == -1:
            if restartbutton.draw():
                player.reset(100, window_height - 80)
                gameover = 0

        
    
    for close in pygame.event.get():
        if close.type == pygame.QUIT:
            gamerun = False

    pygame.display.update()

pygame.quit()


