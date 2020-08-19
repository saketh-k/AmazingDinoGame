import pygame
import random

# DINO_CROUCHED_DIM: 25, 25
# DINO_UPRIGHT_DIM: 50, 25

MIN_HEIGHT = 20
MAX_HEIGHT = 130
MIN_WIDTH = 29
MAX_WIDTH = 30
INIT_SPEED = 10


class GameModel:
    def __init__(self):
        self.tick = 0
        self.dino_score = 0
        self.toNextCactus = 50
        self.speed = INIT_SPEED
        self.cacti = []
        self.ptero = []
        self.sinceLastCactus = 0
        self.dino = Dinosaur(50, 25)
        self.game_over = False

    def makeNewCactus(self):
        width = random.randrange(MIN_WIDTH, MAX_WIDTH)
        height = random.randrange(MIN_HEIGHT, MAX_HEIGHT)
        self.cacti.append(Cactus(height, width))

    def makeNewPtero(self):
        self.ptero.append(Pterodactyl(30, 60, random.randrange(370, 475)))

    def check_collisions(self):
        for cactus in self.cacti:
            if self.dino.rect.colliderect(cactus.rect):
                self.game_over = True
        for ptero in self.ptero:
            if self.dino.rect.colliderect(ptero.rect):
                self.game_over = True

    def doTick(self):
        self.tick += 1
        if self.tick % 500 == 0:
            self.speed += 5
        self.toNextCactus -= 1
        if self.toNextCactus <= 0:
            self.makeNewCactus()
            self.toNextCactus = random.randrange(30, 100)
        self.sinceLastCactus += 1
        self.dino_score += 1
        self.dino.do_tick()
        if self.sinceLastCactus > 50:
            self.sinceLastCactus = 0
            self.makeNewPtero()
        for cactus in self.cacti:
            cactus.move_left(self.speed)
        for pterodactyl in self.ptero:
            pterodactyl.move_left(self.speed * 1.1 + 10)
        self.check_collisions()


class Dinosaur:
    def __init__(self, height, width):
        self.standing_image = pygame.image.load(r'DINO.png').convert()
        self.crouching_image = pygame.image.load(r'DINOCROUCH.png').convert()
        self.standing_image.set_colorkey((255, 255, 255))
        self.crouching_image.set_colorkey((255, 255, 255))
        self.image = self.standing_image
        self.accel = 2
        self.jump_height = 0
        self.height = height
        self.width = width
        self.rect = pygame.Rect(200, 500 - height, width, height)
        self.vel = 0

    def start_squat(self):
        self.image = self.crouching_image
        self.height = 25
        self.width = 25
        self.rect = pygame.Rect(200, 500 - self.height, self.width, self.height)

    def stop_squat(self):
        self.image = self.standing_image
        self.height = 50
        self.width = 25
        self.rect = pygame.Rect(200, 500 - self.height, self.width, self.height)

    def do_tick(self):
        if self.jump_height >= 0 and self.vel != -21:
            self.jump_height = 0
            self.vel = 0
        self.jump_height += self.vel
        self.rect.move_ip(0, self.vel)
        if self.jump_height <= 0:
            self.vel += self.accel
        self.rect = pygame.Rect(200, 500 - self.height + self.jump_height, self.width, self.height)

    def jump(self, init_vel):
        if self.jump_height == 0:
            self.vel = init_vel


class Pterodactyl:
    def __init__(self, height, width, y):
        self.image = pygame.image.load("PTERO.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.height = height
        self.width = width
        self.rect = pygame.Rect(800, y - height, width, height)

    def move_left(self, amount):
        self.rect.move_ip(-amount, 0)


class Cactus:
    def __init__(self, height, width):
        self.image = pygame.image.load("CACTUS.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.height = height
        self.width = width
        self.rect = pygame.Rect(800, 500 - height, width, height)

    def move_left(self, amount):
        self.rect.move_ip(-amount, 0)
