import pygame
from pygame.locals import *

pygame.init()

window_width = 500
window_height = 500

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Birdie Platform')


#load images
sun_picture = pygame.image.load(phil-botha-wgAf3-K94DQ-unsplash.jpg)

gamerun = True
while gamerun:
    for close in pygame.event.get():
        if close.type == pygame.QUIT:
            gamerun = False

pygame.quit()


