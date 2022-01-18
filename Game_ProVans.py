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
    if colorkey is not None:  # определение альфа канала
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = 960, 780
screen = pygame.display.set_mode(size)

# группы спрайтов
all_sprites = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
monet_group = pygame.sprite.Group()

# словарь изображений
tile_image = {'wall': load_image('камни.png'),
              'empty': load_image('газон.jpg'),
              'exit': load_image('выход.png', -1),
              'game': load_image('game.png', -1)}

# константы
tile_width = tile_height = 60
screen_rect = (0, 0, width, height)
GRAVITY = 1


class Sprite(pygame.sprite.Sprite):  # главный класс спрайтов
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):  # неподвижные объекты
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def get_pos(self):
        return self.pos


class Player(Sprite):  # игрок
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super().__init__(player_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 7, tile_height * pos_y + 7)
        self.pos = (pos_x, pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x + 7,
                                               tile_height * y + 7)
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def get_pos(self):
        return self.pos


class AnimatedSprite(pygame.sprite.Sprite):  # монета
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(monet_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.pos = (x, y)

    def cut_sheet(self, sheet, columns, rows, x, y):
        self.rect = pygame.Rect(x * 60, y * 60, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def get_pos(self):
        return self.pos


class Particle(pygame.sprite.Sprite):  # частицы
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def start_screen():  # начальный экран
    intro_text = ["Игра \"Ходилка\"", '',
                  "Герой двигается",
                  "Собирай монеты",
                  'Найди выход',
                  'created by PVS']
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 66
    for line in intro_text:
        string_rendered = font.render(line, True, (128, 5, 128))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_level(filename):  # загрузка уровня
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):  # отрисовка уровня
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(load_image('человек_up.jpg', -1), 9, 1, x, y)
            elif level[y][x] == '!':
                exiti = Tile('exit', x, y)
            elif level[y][x] == 'g':
                gaming = Tile('game', x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y)
                monet = AnimatedSprite(pygame.transform.scale(load_image('moneta.png', -1), (400, 60)), 7, 1, x, y)
    return new_player, monet, exiti, gaming, x, y


def move(hero, movement):  # движение героя
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] != '#':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y <= max_y - 1 and level_map[y + 1][x] != '#':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] != '#':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x <= max_x - 1 and level_map[y][x + 1] != '#':
            hero.move(x + 1, y)


def create_particles(position):  # генерация частиц
    # количество создаваемых частиц
    particle_count = 30
    # возможные скорости
    numbers = range(-7, 7)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


if __name__ == '__main__':
    pygame.display.set_caption('Ходилка')
    player = None

    # итоги
    kol_vo_monet = 0
    kol_plays = 0

    start_screen()

    # цикл уровней
    for level in ['map.txt', 'map1.txt', 'map2.txt']:
        out = False
        running = True

        # переопределение групп
        all_sprites = pygame.sprite.Group()
        sprite_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        monet_group = pygame.sprite.Group()

        clock = pygame.time.Clock()
        level_map = load_level(level)
        hero, monet, exiti, gaming, max_x, max_y = generate_level(level_map)

        # игровой цикл уровня
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if hero.get_pos() == monet.get_pos():
                            print('ok')
                            kol_vo_monet += 1
                            create_particles([x * 60 for x in monet.get_pos()])
                            monet.kill()
                        elif hero.get_pos() == exiti.get_pos():
                            print('go out')
                            out = True
                        elif hero.get_pos() == gaming.get_pos():
                            print('go play')
                            kol_plays += 1
                            create_particles([x * 60 for x in gaming.get_pos()])
                            os.startfile('mini_game_ProVans.py')
            if out:
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                move(hero, 'up')
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                move(hero, 'down')
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                move(hero, 'left')
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                move(hero, 'right')

            # обонвление
            monet_group.update()
            all_sprites.update()
            screen.fill((0, 0, 0))

            # отрисовка
            sprite_group.draw(screen)
            player_group.draw(screen)
            monet_group.draw(screen)
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(15)

    # конец игры
    running = True
    size = width, height = 1000, 200
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        font = pygame.font.Font(None, 50)
        text = font.render(f"Спасибо за игру! Собрано монет: {kol_vo_monet}, мини-игр сыграно {kol_plays}", True,
                           (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)
        pygame.display.flip()
    pygame.quit()
