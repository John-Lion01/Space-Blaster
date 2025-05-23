import pygame
import sys
from Space_Blaster import draw_text, draw_centered_text

WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test level shower !")

# COLORS 
COLORS = {
    'BLACK' : (0, 0, 0),
    'WHITE' : (255, 255, 255),
    'GREEN' : (0, 255, 0),
    'BLUE_NAVY' : (0, 0, 128),
    'BLEU_NUIT' : (10, 10, 30),
    'BLEU_CLAIRE' : (0, 255, 255),
    'VERT_VIF' : (0, 200, 0),
    'GRIS_FONCE' : (60, 60, 60),
    'GRIS_CLAIRE' : (200, 200, 200),
    'RED' : (255, 0, 0),
    'BLUE_SKY' : (0, 191, 255),
    'VIOLET' : (128, 0, 128),
    'YELLOW' : (255, 255, 0),
    'BLEU_TRES_FONCE' : (0, 0, 30)
}

while 1:
    
    
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        pygame.display.flip()