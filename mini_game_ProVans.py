import pygame
import os
import sys
import random


def load_image(name, colorkey=None):  # загрузка изображения
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bird(pygame.sprite.Sprite):  # птички
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('птичка.png')
        self.rect = self.image.get_rect().move(x, y)
        self.vx = random.randint(-7, 7)
        self.vy = random.randrange(-7, 7)

    def update(self, *args):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.kill()

    def get_event(self, event):
        self.update(event)


class Border(pygame.sprite.Sprite):  # стены
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def get_event(self, event):
        pass


def draw(screen):  # надпись
    font = pygame.font.Font(None, 50)
    text = font.render("Победа, можно идти дальше!", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


pygame.init()
size = width, height = 600, 600
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Поймай меня, если сможешь!')
running = True
clock = pygame.time.Clock()

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)
flag = True
for i in range(15):
    Bird(100, 100)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bolls in all_sprites:
                bolls.get_event(event)
    all_sprites.update(event)
    if len(all_sprites.sprites()) == 4:
        draw(screen)
        flag = False
    if flag:
        screen.fill((77, 77, 0))
    all_sprites.draw(screen)
    clock.tick(90)
    pygame.display.flip()
pygame.quit()
