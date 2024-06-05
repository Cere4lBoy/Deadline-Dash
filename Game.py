import sys
import math
import random
import pygame
from scripts.utils import load_image, load_images, Animation
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from button import Button
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.pyvidplayer import Video

def scale_image(image, scale_factor):
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Deadline Dash')
        self.screen = pygame.display.set_mode((1366, 768))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        # Load menu assets and capture returned values
        logo_img, logo_width, logo_height = self.load_menu_assets()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation([scale_image(img, 0.4) for img in load_images('entities/enemy/idle')], img_dur=6),
            'enemy/run': Animation([scale_image(img, 0.4) for img in load_images('entities/enemy/run')], img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)

        # Storing logo_img and logo dimensions
        self.logo_img = logo_img
        self.logo_width = logo_width
        self.logo_height = logo_height

        self.load_level(0)

        self.vid = Video('data/group7intro.mp4')
        self.vid.set_size((1366, 768))
        self.video_playing = True

    def load_menu_assets(self):
        # B.L.O.A.T (Best Logo Of All Time)
        logo_img = pygame.image.load('data/images/DEADLINEDASHLOGO.png').convert_alpha()
        logo_width = int(logo_img.get_width() * 0.3)
        logo_height = int(logo_img.get_height() * 0.3)
        logo_img = pygame.transform.scale(logo_img, (logo_width, logo_height))

        # Load button images
        start_img = pygame.image.load('data/images/menubuttons/START.png').convert_alpha()
        exit_img = pygame.image.load('data/images/menubuttons/EXIT.png').convert_alpha()
        leaderb_img = pygame.image.load('data/images/menubuttons/LEADERBOARD.png').convert_alpha()
        credits_img = pygame.image.load('data/images/menubuttons/CREDITS.png').convert_alpha()

        # Background Image
        self.background_img = pygame.image.load('data/images/MENUBG.png').convert()

        # Button objects
        self.start_button = Button(800, 300, start_img, 0.7)
        self.exit_button = Button(800, 400, exit_img, 0.7)
        self.leaderb_button = Button(800, 200, leaderb_img, 0.5)
        self.credits_button = Button(800, 500, credits_img, 0.7)

        return logo_img, logo_width, logo_height

    def draw_menu(self):
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.logo_img, (50, (self.screen.get_height() - self.logo_height) // 2))  # Center logo vertically

        # Draw buttons and handle actions
        if self.start_button.draw(self.screen):
            self.run_game()
        if self.exit_button.draw(self.screen):
            pygame.quit()
            sys.exit()
        if self.leaderb_button.draw(self.screen):
            pass
        if self.credits_button.draw(self.screen):
            pass

        pygame.display.update()

    def start_game(self):
        self.menu_running = False

    def run_menu(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.draw_menu()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.menu_running = True


    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0

    def adjust_enemy_position(self, enemy_index, new_position):
        if 0 <= enemy_index < len(self.enemies):
            self.enemies[enemy_index].pos = new_position

    def play_intro_video(self):
        self.vid.restart()  # Ensure the video starts from the beginning
        while self.vid.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.vid.active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.vid.active = False

            self.screen.fill((0, 0, 0))
            self.vid.draw(self.screen, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        self.play_intro_video()  # Play the video once at the start
        self.run_menu()  # Run the menu
    def run_game(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_level(0)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap)  # Removed movement argument
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            movement = [0, 0]  # Initialize movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                movement[0] -= 2  # Adjust movement speed as needed
            if keys[pygame.K_RIGHT]:
                movement[0] += 2  # Adjust movement speed as needed

            if not self.dead:
                self.player.update(self.tilemap, movement=movement)
                self.player.render(self.display, offset=render_scroll, timer=self.dead)

            for projectile in self.projectiles.copy():
                img = self.assets['projectile']
                projectile[0][0] += math.cos(projectile[1]) * 8
                projectile[0][1] += math.sin(projectile[1]) * 8
                projectile[2] += 1
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
Game().run()
