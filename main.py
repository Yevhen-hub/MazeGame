from pygame import *
import random

init()
font.init()

size = (500, 500)
window = display.set_mode(size)
display.set_caption('Лабіринт')
clock = time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

background_images = ['background.jpg', 'background2.png', 'background3.png', 'background4.png', 'background_boss.png']


class Background:
    def __init__(self, img):
        self.image = transform.scale(image.load(img),size)

    def draw(self):
        window.blit(self.image, (0, 0))


class GameSprite:
    def __init__(self, img, x, y, width, height):
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= 5
        if keys[K_s] and self.rect.y < 450:
            self.rect.y += 5
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[K_d] and self.rect.x < 450:
            self.rect.x += 5


class Wall:
    def __init__(self, x, y, width, height, color):
        self.rect = Rect(x, y, width, height)
        self.color = color

    def reset(self):
        draw.rect(window, self.color, self.rect)


class Enemy(GameSprite):
    def __init__(self, img, x, y, width, height, start_x, end_x):
        super().__init__(img, x, y, width, height)
        self.start_x = start_x
        self.end_x = end_x
        self.direction = True

    def update(self):
        if self.rect.x >= self.end_x:
            self.direction = False
        if self.rect.x <= self.start_x:
            self.direction = True

        if self.direction:
            self.rect.x += 5
        else:
            self.rect.x -= 5


class Sword(GameSprite):
    def __init__(self, img, x, y, width, height):
        super().__init__(img, x, y, width, height)
        self.thrown = False
        self.speed = 10

    def update(self):
        if self.thrown:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.thrown = False
                self.rect.x = -100

    def throw(self, x, y):
        if not self.thrown:
            self.rect.x = x
            self.rect.y = y
            self.thrown = True


class Boss(GameSprite):
    def __init__(self, img, x, y, width, height):
        super().__init__(img, x, y, width, height)
        self.hp = 10  # Boss has 10 HP

    def update(self):
        if self.hp > 0:
            self.rect.x += random.choice([-2, 2])
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.x > 450:
                self.rect.x = 450

    def take_damage(self):
        self.hp -= 1

class FallingWall(Wall):
    def update(self):
        self.rect.y += 3
        if self.rect.y > 500:
            self.rect.y = -random.randint(100, 500)


def create_walls(level):
    walls = []
    if level == 1:
        position_walls = [(100, 100), (160, 0), (220, 60), (220, 60)]
        size_walls = [(5, 400), (5, 400), (5, 400), (200, 5)]
    elif level == 2:
        position_walls = [(50, 50), (150, 150), (300, 100), (350, 300)]
        size_walls = [(5, 200), (5, 300), (300, 5), (5, 200)]
    elif level == 3:
        position_walls = [(100, 100), (160, 0), (300, 200), (350, 400)]
        size_walls = [(5, 400), (200, 5), (5, 200), (5, 100)]
    elif level == 4:
        position_walls = [(100, 200), (400, 50), (100, 400), (100, 400)]
        size_walls = [(5, 300), (5, 300), (300, 5), (300, 5)]
    elif level == 5:
        position_walls = []
        size_walls = []

#        for _ in range(5):
#           walls.append(FallingWall(random.randint(0, 450), random.randint(-500, -50), 50, 10, RED))

    else:
        return []

    for i in range(len(size_walls)):
        x = position_walls[i][0]
        y = position_walls[i][1]
        width = size_walls[i][0]
        height = size_walls[i][1]
        wall = Wall(x, y, width, height, RED)
        walls.append(wall)
    return walls


def create_enemies(level):
    if level == 1:
        return [Enemy('cyborg.png', 240, 120, 50, 50, 240, 450)]
    elif level == 2:
        return [
            Enemy('cyborg.png', 240, 120, 50, 50, 240, 450),
            Enemy('cyborg.png', 100, 200, 50, 50, 100, 400)
        ]
    elif level == 3:
        return [
            Enemy('cyborg.png', 240, 120, 50, 50, 240, 450),
            Enemy('cyborg.png', 100, 200, 50, 50, 100, 400),
            Enemy('cyborg.png', 300, 300, 50, 50, 300, 450)
        ]
    elif level == 4:
        return [
            Enemy('cyborg.png', 240, 120, 50, 50, 240, 450),
            Enemy('cyborg.png', 100, 200, 50, 50, 100, 400),
            Enemy('cyborg.png', 300, 300, 50, 50, 300, 450),
            Enemy('cyborg.png', 200, 150, 50, 50, 200, 450)
        ]
    elif level == 5:
        return [Boss('boss.png', 200, 50, 100, 100)]

player = Player('hero.png', 20, 400, 50, 50)
finish = GameSprite('treasure.png', 400, 400, 50, 50)
font1 = font.Font(None, 30)

hp = 10
level = 1
background = Background(background_images[level - 1])
walls = create_walls(level)
enemies = create_enemies(level)
sword = Sword('sword.png', -100, -100, 50, 50)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and level == 5:
                sword.throw(player.rect.x + 25, player.rect.y)

    background.draw()

    player.reset()
    player.update()
    finish.reset()

    for wall in walls:
        wall.reset()
        if isinstance(wall, FallingWall):
            wall.update()
        if wall.rect.colliderect(player):
            player.rect.x = 20
            player.rect.y = 400
            hp -= 1

    for enemy in enemies:
        enemy.reset()
        enemy.update()
        if isinstance(enemy, Boss) and enemy.hp > 0:
            if sword.rect.colliderect(enemy):
                enemy.take_damage()
                sword.thrown = False
        if enemy.rect.colliderect(player):
            player.rect.x = 20
            player.rect.y = 400
            hp -= 1

    sword.reset()
    sword.update()

    text_hp = font1.render(f'HP: {hp}', True, BLACK)
    window.blit(text_hp, (20, 20))

    if hp <= 0:
        window.fill(RED)
        game = False

    if finish.rect.colliderect(player):
        if level <= 5:
            level += 1
            background = Background(background_images[level - 1])
            walls = create_walls(level)
            enemies = create_enemies(level)
            player.rect.x = 20
            player.rect.y = 400
        else:
            window.fill(GREEN)
            game = False

    display.update()
    clock.tick(60)