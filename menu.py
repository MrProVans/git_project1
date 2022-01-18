import pygame
import os


def draw(screen):
    font = pygame.font.Font(None, 35)
    text = font.render("Счет в уме!", True, (100, 255, 100))
    text_x = width // 3 - text.get_width() // 2
    text_y = height // 3 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    text1 = font.render("Ходилка!", True, (100, 255, 100))
    text_x1 = width // 1.5 - text.get_width() // 2
    text_y1 = height // 3 - text.get_height() // 2
    screen.blit(text1, (text_x1, text_y1))


pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Menu game')
screen.fill((100, 100, 100))
running = True
pygame.draw.rect(screen, (255, 160, 37), (100, 260, 150, 100), 0)
pygame.draw.rect(screen, (170, 0, 170), (320, 260, 150, 100), 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if 100 < x < 250 and 260 < y < 360:
                os.startfile('Игра. Счёт в уме.py')
            elif 320 < x < 470 and 260 < y < 360:
                os.startfile('Game_ProVans.py')
    draw(screen)
    pygame.display.flip()
pygame.quit()