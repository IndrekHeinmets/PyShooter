import button
import csv
import level_editor
import os
import pygame
import random
import time

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 512)
pygame.init()

# Screen settings
WIDTH = 900
HEIGHT = int(WIDTH * 0.8)
SOLIDER_SCALE = 1.6
FPS = 120

# Dynamics settings
PLAYER_SPEED = 4
JUMP_SPEED = 13
ENEMY_SPEED = 2
ENEMY_VISION_RANGE = 200
GRAVITY = 0.75
BULLET_SPEED = 10
GRENADE_X_SPEED, GRENADE_Y_SPEED = 7, -11
MINE_X_SPEED, MINE_Y_SPEED = 1, 1

# World variables
ROWS = 16
COLS = 150
TILE_SIZE = HEIGHT // ROWS
TILE_TYPES = 22
LEVEL = 1
MAX_LEVELS = 2
start_game = False
start_intro = False

# Scroll variables
SCROLL_THRESH = 200
screen_scroll = 0
bg_scroll = 0

# Damage settings
BULLET_DAMAGE_PLAYER = 5
BULLET_DAMAGE_ENEMY = 25
GRENADE_DAMAGE_RANGE = [1, 2, 3] # tiles
GRENADE_DAMAGE = [50, 30, 10] # corresponds to distance
MINE_DAMAGE_RANGE = [1, 2, 3, 4, 5] # tiles
MINE_DAMAGE = [95, 80, 50, 30, 15] # corresponds to distance

# Item box addition settings
HEALTH_BOX = 30
AMMO_BOX = 20
GRENADE_BOX = 3
MINE_BOX = 2

# Colors
BG = (0, 194, 162)
PINK = (235, 65, 54)
GREEN = (0, 255, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 194, 162)
RED = (200, 25, 25)

# Actions
IDLE = 0
RUN = 1
JUMP = 2
DEATH = 3

# Font
FONT = pygame.font.SysFont('Futura', 28)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PyShooter by Inz')
clock = pygame.time.Clock()

# player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
mine = False
mine_planted = False

# Load music/sounds
jump_fx = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\Python\\Platformer\\audio\\jump.wav')
jump_fx.set_volume(0.2)
shot_fx = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\Python\\Platformer\\audio\\shot.wav')
shot_fx.set_volume(0.2)
explosion_fx = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\Python\\Platformer\\audio\\grenade.wav')
explosion_fx.set_volume(0.2)
pickup_fx = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\Python\\Platformer\\audio\\pickup.wav')
pickup_fx.set_volume(0.2)
water_fx = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\Python\\Platformer\\audio\\water.wav')
water_fx.set_volume(0.2)
death_fx = pygame.mixer.Sound('C:\\Users\\inzah\\Documents\\Python\\Platformer\\audio\\oof.wav')
water_fx.set_volume(0.2)

# Load images:
# button images
start_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\start_btn.png').convert_alpha()
restart_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\restart_btn.png').convert_alpha()
exit_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\exit_btn.png').convert_alpha()
editor_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\editor_btn.png').convert_alpha()
menu_btn_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\menu_btn.png').convert_alpha()
exit_to_menu_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\exit_to_menu.png').convert_alpha()
resume_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\resume_btn.png').convert_alpha()
pause_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\pause_btn.png').convert_alpha()
# bg images
sky_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\background\\sky.png').convert_alpha()
mountain_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\background\\mountain.png').convert_alpha()
pine1_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\background\\pine1.png').convert_alpha()
pine2_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\background\\pine2.png').convert_alpha()
# title pages
menu_bg_img = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\menu_bg.png').convert_alpha(), (WIDTH, HEIGHT))
pause_bg_img = pygame.transform.scale(pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\pause_bg.png').convert_alpha(), (WIDTH, HEIGHT))
# tiles
tile_img_list = []
for i in range(TILE_TYPES):
    img = pygame.transform.scale(pygame.image.load(f'C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\tile\\{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
    tile_img_list.append(img)
# ammo
bullet_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\icons\\bullet.png').convert_alpha()
grenade_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\icons\\grenade.png').convert_alpha()
mine_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\icons\\mine.png').convert_alpha()
# pickups
health_box_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\icons\\health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\icons\\ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\icons\\grenade_box.png').convert_alpha()
mine_box_img = pygame.image.load('C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\icons\\mine_box.png').convert_alpha()
item_boxes = {
    'Health' : health_box_img,
    'Ammo' : ammo_box_img,
    'Grenade' : grenade_box_img,
    'Mine' : mine_box_img
}

# Create empty world data list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# Load in created level data
with open(f'C:\\Users\\inzah\\Documents\\Python\\Platformer\\levels\\level{LEVEL}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for i in range(5):
        screen.blit(sky_img, ((i * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((i * width) - bg_scroll * 0.6, HEIGHT - mountain_img.get_height() - 250))
        screen.blit(pine1_img, ((i * width) - bg_scroll * 0.8, HEIGHT - pine1_img.get_height() - 120))
        screen.blit(pine2_img, ((i * width) - bg_scroll * 0.9, HEIGHT - pine2_img.get_height()))

def load_level():
    with open(f'C:\\Users\\inzah\\Documents\\Python\\Platformer\\levels\\level{LEVEL}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = World()
    player, health_bar = world.process_data(world_data)
    return world, player, health_bar

def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # reset world data (reload)
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

class Solider(pygame.sprite.Sprite):
    def __init__(self, x, y, type, scale, speed, ammo, grenades, mines):
        pygame.sprite.Sprite.__init__(self)
        # common solider variables
        self.alive = True
        self.type = type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.mines = mines
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.in_air = True
        self.jump = False
        self.flip = False
        self.anim_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, ENEMY_VISION_RANGE, 20)
        self.idle = False
        self.idle_counter = 0

        # Load all player images
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for type in animation_types:
            temp_list = []
            # Count files in folder
            num_of_frames = len(os.listdir(f'C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\{self.type}\\{type}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\{self.type}\\{type}\\{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.anim_list.append(temp_list)
        self.image = self.anim_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_anim()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx, dy = 0, 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            self.flip = False
            self.direction = 1
            dx = self.speed

        if self.jump and not self.in_air:
            self.vel_y = -JUMP_SPEED
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Obstacle collision
        for tile in world.obstacle_list:
            # x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # if wall collision, turn around
                if self.type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # in air
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # water collision
        if pygame.sprite.spritecollide(self, water_group, False):
            water_fx.play()
            self.rect.y += self.height // 2
            self.health = 0

        # fallen off-map
        if self.rect.top > HEIGHT:
            self.health = 0

        # Check if off-screen
        if self.type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
                dx = 0

        # Check level end (exit)
        level_complete = False
        if self.type == 'player':
            if pygame.sprite.spritecollide(self, exit_group, False):
                level_complete = True

        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll
        if self.type == 'player':
            if (self.rect.right > WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.ammo -= 1
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.7 * self.direction), self.rect.centery, self.direction)
            shot_fx.play()
            bullet_group.add(bullet)

    def ai(self):
        # walk around
        if self.alive:
            if not self.idle and random.randint(1, 200) == 1:
                self.update_action(IDLE)
                self.idle = True
                self.idle_counter = 50
            # check if player in vision field and shoot
            if self.vision.colliderect(player.rect) and player.alive:
                self.update_action(IDLE)
                self.shoot()
            else:
                if not self.idle:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(RUN)
                    self.move_counter += 1
                    # update ai vision
                    self.vision.center = (self.rect.centerx + ENEMY_VISION_RANGE / 2 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1

                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idle = False

        # Scroll
        self.rect.x += screen_scroll

    def update_anim(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.anim_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.anim_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.anim_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive =False
            self.update_action(DEATH)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = tile_img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8: # Obstacles
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10: # Water
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 12: # Box
                        self.obstacle_list.append(tile_data)
                    elif tile >= 11 and tile <= 14 and tile != 12: # Decor
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15: # Create player
                        player = Solider(x * TILE_SIZE, y * TILE_SIZE, 'player', SOLIDER_SCALE, PLAYER_SPEED, 100, 5, 2)
                        health_bar = HealthBar(105, HEIGHT - 26, player.health, player.max_health)
                    elif tile == 16: # Create enemy
                        enemy = Solider(x * TILE_SIZE, y * TILE_SIZE, 'enemy', SOLIDER_SCALE, ENEMY_SPEED, 100, 0, 0)
                        enemy_group.add(enemy)
                    elif tile == 17: # Create ammo box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18: # Create grenade box
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19: # Create mine box
                        item_box = ItemBox('Mine', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20: # Create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 21: # Create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height())

    def update(self):
        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        # check player box pickup
        if pygame.sprite.collide_rect(self, player):
            # check box type
            if self.item_type == 'Health':
                pickup_fx.play()
                player.health += HEALTH_BOX
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                pickup_fx.play()
                player.ammo += AMMO_BOX
            elif self.item_type == 'Grenade':
                pickup_fx.play()
                if player.grenades < 6:
                    player.grenades += GRENADE_BOX
                    if player.grenades > 7:
                        player.grenades = 7
            elif self.item_type == 'Mine':
                pickup_fx.play()
                if player.mines < 3:
                    player.mines += MINE_BOX
                    if player.mines > 3:
                        player.mines = 3
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def re_draw(self, health):
        self.health = health
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 16))
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 16))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 150, 16), 3)

class LevelBar():
    def __init__(self, x, y, progress, total_len, level):
        self.x = x
        self.y = y
        self.progress = progress
        self.total_len = total_len
        self.level = level

    def re_draw(self, progress):
        self.progress = progress
        pygame.draw.rect(screen, PINK, (self.x, self.y, (WIDTH - 120), 12))
        ratio = self.progress / self.total_len
        pygame.draw.rect(screen, BLUE, (self.x, self.y, (WIDTH - 120) * ratio, 12))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, (WIDTH - 120), 12), 2)
        player_icon = pygame.transform.scale(tile_img_list[15], (30, 30))
        screen.blit(player_icon, (self.x + ((WIDTH - 170) * ratio), 8))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = BULLET_SPEED
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check if off screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
        # check collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= BULLET_DAMAGE_PLAYER
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= BULLET_DAMAGE_ENEMY
                    self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = GRENADE_Y_SPEED
        self.speed = GRENADE_X_SPEED
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y

        # check level collision
        for tile in world.obstacle_list:
            # wall collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.speed * self.direction
            # y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # in air
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # update position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # countdown to explosion
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, GRENADE_DAMAGE_RANGE[1])
            explosion_group.add(explosion)

            # # do damage to player if nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * GRENADE_DAMAGE_RANGE[0] and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * GRENADE_DAMAGE_RANGE[0]:
                player.health -= GRENADE_DAMAGE[0]
            elif abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * GRENADE_DAMAGE_RANGE[1] and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * GRENADE_DAMAGE_RANGE[1]:
                player.health -= GRENADE_DAMAGE[1]
            elif abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * GRENADE_DAMAGE_RANGE[2] and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * GRENADE_DAMAGE_RANGE[2]:
                player.health -= GRENADE_DAMAGE[2]

            # # do damage to nearby enemies
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * GRENADE_DAMAGE_RANGE[0] and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * GRENADE_DAMAGE_RANGE[0]:
                    enemy.health -= GRENADE_DAMAGE[0]
                elif abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * GRENADE_DAMAGE_RANGE[1] and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * GRENADE_DAMAGE_RANGE[1]:
                    enemy.health -= GRENADE_DAMAGE[1]
                elif abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * GRENADE_DAMAGE_RANGE[2] and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * GRENADE_DAMAGE_RANGE[2]:
                    enemy.health -= GRENADE_DAMAGE[2]

class Mine(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 300
        self.vel_y = MINE_Y_SPEED
        self.speed = MINE_X_SPEED
        self.image = mine_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.exploded = False
        self.in_range = False

    def update(self):
        self.vel_y += GRAVITY
        dx = self.speed * self.direction
        dy = self.vel_y

        # check level collision
        for tile in world.obstacle_list:
            # wall collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.speed * self.direction
            # y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # in air
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # update position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # player collision
        if pygame.sprite.spritecollide(player, mine_group, False):
            if player.alive:
               self.in_range = True

        # check collision with enemy
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, mine_group, False):
                if enemy.alive:
                    self.kill()
                    explosion_fx.play()
                    self.exploded = True
                    explosion = Explosion(self.rect.x, self.rect.y, MINE_DAMAGE_RANGE[1])
                    explosion_group.add(explosion)

                    # # do damage to player if nearby
                    if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[0] and \
                            abs(self.rect.centery - player.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[0]:
                        player.health -= MINE_DAMAGE[0]
                    elif abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[1] and \
                            abs(self.rect.centery - player.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[1]:
                        player.health -= MINE_DAMAGE[1]
                    elif abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[2] and \
                            abs(self.rect.centery - player.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[2]:
                        player.health -= MINE_DAMAGE[2]
                    elif abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[3] and \
                            abs(self.rect.centery - player.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[3]:
                        player.health -= MINE_DAMAGE[3]
                    elif abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[4] and \
                            abs(self.rect.centery - player.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[4]:
                        player.health -= MINE_DAMAGE[4]

                    # # do damage to nearby enemies
                    for enemy in enemy_group:
                        if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[0] and \
                                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[0]:
                            enemy.health -= MINE_DAMAGE[0]
                        elif abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[1] and \
                                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[1]:
                            enemy.health -= MINE_DAMAGE[1]
                        elif abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[2] and \
                                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[2]:
                            enemy.health -= MINE_DAMAGE[2]
                        elif abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[3] and \
                                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[3]:
                            enemy.health -= MINE_DAMAGE[3]
                        elif abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * MINE_DAMAGE_RANGE[4] and \
                                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * MINE_DAMAGE_RANGE[4]:
                            enemy.health -= MINE_DAMAGE[4]

        return self.exploded, self.in_range

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.anim_list = []
        for i in range(1, 6):
            img = pygame.image.load(f'C:\\Users\\inzah\\Documents\\Python\\Platformer\\img\\explosion\\{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.anim_list.append(img)
        self.frame_index = 0
        self.image = self.anim_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #scroll
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 8
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter =0
            self.frame_index += 1
            if self.frame_index >= len(self.anim_list):
                self.kill()
            else:
                self.image = self.anim_list[self.frame_index]

class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: # whole screen fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, WIDTH // 2, HEIGHT))
            pygame.draw.rect(screen, self.color, (WIDTH // 2 + self.fade_counter, 0, WIDTH, HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, WIDTH, HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, HEIGHT // 2 + self.fade_counter, WIDTH, HEIGHT))

        if self.direction == 2: # vertical fade down
            pygame.draw.rect(screen, self.color, (0, 0, WIDTH, 0 + self.fade_counter))
            if self.fade_counter >= WIDTH:
                fade_complete = True

        return fade_complete

# Fades
intro_fade = ScreenFade(1, BLACK, 5)
death_fade = ScreenFade(2, PINK, 5)

# Buttons
start_button = button.Button(WIDTH // 2 - 110, HEIGHT // 2 - 40, start_img, 0.8)
restart_button = button.Button(WIDTH // 2 - 155, HEIGHT // 2 + 25, restart_img, 0.9)
exit_button = button.Button(WIDTH // 2 - 75, HEIGHT // 2 + 180, exit_img, 0.7)
editor_button = button.Button(WIDTH // 2 - 155, HEIGHT // 2 + 65, editor_img, 0.9)
menu_button = button.Button(WIDTH // 2 - 100, HEIGHT // 2 - 200, menu_btn_img, 0.7)
pause_button = button.Button(15, 45, pause_img, 0.07)
resume_button = button.Button(WIDTH // 2 - (resume_img.get_width() * 0.8) // 2, 480, resume_img, 0.8)
exit_to_menu_button = button.Button(WIDTH - (exit_to_menu_img.get_width() * 0.6) - 25, HEIGHT - 80, exit_to_menu_img, 0.6)

# Sprite groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
mine_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world = World()
player, health_bar = world.process_data(world_data)
level_bar = LevelBar(105, 20, bg_scroll, ((world.level_length * TILE_SIZE) - WIDTH), LEVEL)

run = True
paused = False
while run:
    clock.tick(FPS)

    if not start_game and paused:
        screen.blit(pause_bg_img, (0, 0, WIDTH, HEIGHT))
        if resume_button.draw(screen):
            pygame.draw.rect(screen, RED, resume_button.rect, 3)
            time.sleep(0.2)
            paused = False
            start_game = True
        if exit_to_menu_button.draw(screen):
            pygame.draw.rect(screen, RED, exit_to_menu_button.rect, 3)
            time.sleep(0.2)
            paused = False
            start_game = False
            continue
    elif not start_game:
        # Draw menu
        screen.blit(menu_bg_img, (0, 0, WIDTH, HEIGHT))
        # Buttons
        if start_button.draw(screen):
            pygame.draw.rect(screen, RED, start_button.rect, 3)
            time.sleep(0.2)
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            pygame.draw.rect(screen, RED, exit_button.rect, 3)
            break
        if editor_button.draw(screen):
            pygame.draw.rect(screen, RED, editor_button.rect, 3)
            time.sleep(0.2)
            game = level_editor.MainGame()
            quit, menu = game.editor_play()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Shooter by IndrekHe.')

            # Quit whole program when editor is quit or return to main menu
            if not quit and not menu:
                run = False
            elif not quit and menu:
                continue

    else:
        # Update bg
        draw_bg()
        # Draw world
        world.draw()
        # update and draw groups
        bullet_group.update()
        grenade_group.update()
        mine_group.update()
        item_box_group.update()
        decoration_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        exit_group.draw(screen)
        grenade_group.draw(screen)
        mine_group.draw(screen)
        # Show player health
        health_bar.re_draw(player.health)
        level_bar.re_draw(bg_scroll)

        # Draw player
        player.update()
        player.draw()

        # Draw enemies
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        # Draw water and explosions
        water_group.update()
        explosion_group.update()
        water_group.draw(screen)
        explosion_group.draw(screen)

        health_bar.re_draw(player.health)
        level_bar.re_draw(bg_scroll)

        # Pause game
        if pause_button.draw(screen):
            time.sleep(0.2)
            start_game = False
            paused = True

        # Show ammo
        draw_text(f'AMMO: {player.ammo}', FONT, WHITE, 300, HEIGHT - 28)
        # Show grenades
        draw_text(f'FRAGS:', FONT, WHITE, 438, HEIGHT - 28)
        if player.grenades == 0:
            draw_text('0', FONT, WHITE, 520, HEIGHT - 28)
        for x in range(player.grenades):
            scaled_img = pygame.transform.scale(grenade_img, (14, 17))
            screen.blit(scaled_img, (520 + (x * 21), HEIGHT - 28))
        # Show mines
        draw_text(f'MINES:', FONT, WHITE, 680, HEIGHT - 28)
        if player.mines == 0:
            draw_text('0', FONT, WHITE, 755, HEIGHT - 28)
        for x in range(player.mines):
            scaled_img = pygame.transform.scale(mine_img, (34, 8))
            screen.blit(scaled_img, (755 + (x * 40), HEIGHT - 20))
        # Show health
        draw_text(f'HEALTH:', FONT, WHITE, 15, HEIGHT - 28)
        # Show level
        draw_text(f'LEVEL {LEVEL}: ', FONT, BLACK, 15, 16)
        exit_icon = pygame.transform.scale(tile_img_list[21], (25, 25))
        screen.blit(exit_icon, (WIDTH - 30, 12))

        # Show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        if player.alive:
            if shoot:
                player.shoot()
            elif grenade and not grenade_thrown and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (player.rect.size[0] * 0.5 * player.direction), player.rect.top, player.direction)
                grenade_group.add(grenade)
                grenade_thrown = True
                player.grenades -= 1
            elif mine and not mine_planted and player.mines > 0:
                mine = Mine(player.rect.centerx + (player.rect.size[0] * 0.5 * player.direction), player.rect.top, player.direction)
                mine_group.add(mine)
                mine_planted = True
                player.mines -= 1

            if player.in_air:
                player.update_action(JUMP)
            elif moving_left or moving_right:
                player.update_action(RUN)
            else:
                player.update_action(IDLE)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # completed the level
            if level_complete:
                start_intro = True
                LEVEL += 1
                bg_scroll = 0
                world_data = reset_level()
                if LEVEL <= MAX_LEVELS:
                    # Load
                    world, player, health_bar = load_level()
        else:
            death_fx.play()
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    pygame.draw.rect(screen, RED, restart_button.rect, 3)
                    time.sleep(0.2)
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    # Load
                    world, player, health_bar = load_level()
                if menu_button.draw(screen):
                    pygame.draw.rect(screen, RED, menu_button.rect, 3)
                    time.sleep(0.2)
                    start_game = False
                    continue

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Keyboard keys pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_e:
                for mine in mine_group:
                    exploded, in_range = mine.update()
                    if exploded == False and in_range == True:
                        player.mines += 1
                        mine.kill()
                    elif not exploded and not in_range:
                        mine_group.empty()
                        mine = True
                mine_group.empty()
                mine = True

        # Keyboard keys released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade_thrown = False
                grenade = False
            if event.key == pygame.K_e:
                mine_planted = False
                mine = False

    pygame.display.update()
