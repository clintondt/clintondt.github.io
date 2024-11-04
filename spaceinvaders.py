import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image
class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        alien = SpriteSheet("player.png")
        self.image = alien.get_image(150, 0, 40, 40)
        self.rect = self.image.get_rect()
        self.xspeed = 0
    def move(self):
        if direction == 1:
            self.rect.x += 1
class Player(Block):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.image = pygame.Surface([width, height])
        player = SpriteSheet("player.png")
        self.image = player.get_image(0,0,100,45)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.xspeed = 0
    def update(self):
        if self.rect.x < 620 and self.rect.x > 0:
            self.rect.x += self.xspeed
        if self.rect.x < 0:
            self.rect.x = 1
        elif self.rect.x > 620:
            self.rect.x = 619
class Bullet(Block):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.image = pygame.Surface([width, height])
        player = SpriteSheet("player.png")
        self.image = player.get_image(200,0,10,20)
        self.rect = self.image.get_rect()
class Arrow(Block):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.image = pygame.Surface([width,height])
        player = SpriteSheet("player.png")
        self.image = player.get_image(210,0,10,15)
        self.rect = self.image.get_rect()
def drawlives(lives):
    player = SpriteSheet("player.png")
    if lives == 3:
        image = player.get_image(220,0,87,29)
    elif lives == 2:
        image = player.get_image(220,0,58,29)
    else:
        image = player.get_image(220,0,29,29)
    screen.blit(image, [130,637])
pygame.init()

screen_width = 720
screen_height = 672
screen = pygame.display.set_mode([screen_width, screen_height])
direction = 1
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
bullet_kill_list = pygame.sprite.Group()
all_bullet_list = pygame.sprite.Group()
arrow_list = pygame.sprite.Group()
arrow_kill_list = pygame.sprite.Group()
background = pygame.image.load('background.png')

def reset():
    for x in range(20, 520, 55):
        for y in range(50, 280, 70):    
            block = Block(RED, 50, 50)
            block.rect.y = y
            block.rect.x = x
            block_list.add(block)
            all_sprites_list.add(block)
    kill = 0
kill = 0
reset()

player = Player(RED, 100, 45)
player.rect.x = 100
player.rect.y = 575
all_sprites_list.add(player)

done = False
lives = 3
clock = pygame.time.Clock()
counter = 1
score = 0
cooldown = 0

explosion = pygame.mixer.Sound("explosion.wav")
shoot = pygame.mixer.Sound("shoot.wav")
killed = pygame.mixer.Sound("invaderkilled.wav")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.xspeed = -3
            elif event.key == pygame.K_RIGHT:
                player.xspeed = 3
            elif event.key == pygame.K_SPACE:
                if cooldown == 0:
                    pygame.mixer.Sound.play(shoot)
                    bullet = Bullet(RED, 50, 50)
                    bullet.rect.x = player.rect.x + 45
                    bullet.rect.y = player.rect.y - 20
                    all_sprites_list.add(bullet)
                    all_bullet_list.add(bullet)
                    cooldown = 20
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.xspeed = 0
    for bullet in all_bullet_list:
        bullet.rect.y -= 5
    for bullet in bullet_kill_list:
        all_sprites_list.remove(bullet)
    player.update()
    counter += 5
    for block in block_list:
        if counter % 1340 > 670 and direction == 1:
            for block in block_list:
                block.rect.y += 25
            direction = 0
        elif counter % 1340 < 670 and direction == 0:
            for block in block_list:
                block.rect.y += 25
            direction = 1
        elif direction == 1:
            block.rect.x += 0.5
        elif direction == 0:
            block.rect.x -= 1
    for block in block_list:
        ran = random.randint(0,3000)
        if block.rect.y > 535:
            lives = 0
        if ran == 111:
            arrow = Arrow(RED, block.rect.x, block.rect.y)
            arrow.rect.x = block.rect.x
            arrow.rect.y = block.rect.y
            all_sprites_list.add(arrow)
            arrow_list.add(arrow)
    if cooldown > 0:
        cooldown -= 1
    for bullet in all_bullet_list:
        bullet_kill_list = pygame.sprite.groupcollide(all_bullet_list, block_list, True, True)
        for bullet in bullet_kill_list:
            pygame.mixer.Sound.play(killed)
            score += 10
            kill += 1 
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
    for arrow in arrow_list:
        arrow.rect.y += 3
        arrow_kill_list = pygame.sprite.spritecollide(player, arrow_list, True)
        pygame.sprite.groupcollide(all_bullet_list, arrow_list, True, True)
        for arrow in arrow_kill_list:
            lives -= 1
    screen.blit(background, [0, 0])
    pygame.draw.rect(screen, GREEN, [0, 630, 720, 3])
    font = pygame.font.Font("8-bit-hud.ttf", 15)
    text = font.render("LIVES:" ,True,GREEN)
    text2 = font.render("SCORE: " + str(score), True,GREEN)
    screen.blit(text, [10, 642])
    screen.blit(text2, [300, 642])
    drawlives(lives)
    all_sprites_list.draw(screen)
    if lives <= 0:
        pygame.mixer.Sound.play(explosion)
        pygame.time.wait(100)
        done = True
    if kill == 40:
        pygame.time.wait(100)
        done = True
    clock.tick(60)

    pygame.display.flip()
pygame.quit()