import pygame
import sys
from Space_Blaster import draw_text, draw_centered_text

WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test level shower !")

while 1:
    cols = 10
    rows = 15
    bs = 60
    mg = 10
    draw_centered_text("Choisis ton niveau", 30, pygame.font.SysFont(None, 48))
    for i in range(cols*rows) :
        # rang colonne & ligne
        col = i%cols
        row = i//rows
        # x & y
        x = 45 + col * (bs + mg)
        y = 80 + row * (bs + mg)
        rect = pygame.Rect(x, y, bs, bs)
        pygame.draw.rect(screen, (0, 200, 0), rect)
        
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        pygame.display.flip()