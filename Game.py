import os
import sys
import math
import random
import pygame
import json
from Scripts.utils import load_image, load_images, Animation
from Scripts.entities import PhysicsEntity, Player, Enemy
from Scripts.tilemap import Tilemap
from Scripts.clouds import Clouds
from Scripts.particle import Particle
from Scripts.spark import Spark
from Scripts.pyvidplayer import Video

#Sorry for the 600 lines of code
#Provided some comments to briefly shows whats the code for
#Thankyou sir

# Pause menu assets
WHITE = (255, 255, 255, 128)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
resume_button = pygame.Surface((200, 50))
quit_button = pygame.Surface((200, 50))
resume_button.fill(BUTTON_COLOR)
quit_button.fill(BUTTON_COLOR)

pygame.init()
pygame.display.set_caption('Deadline Dash')
screen = pygame.display.set_mode((1366, 768))
resume_button_img = pygame.image.load('data/images/pause_buttons/resumebutton.png').convert_alpha()
quit_button_img = pygame.image.load('data/images/pause_buttons/quitbutton.png').convert_alpha()
clock = pygame.time.Clock()
pygame_icon = pygame.image.load('data/gameicon.png')
pygame.display.set_icon(pygame_icon)

resume_button_img = pygame.transform.scale(resume_button_img, (200, 100))
quit_button_img = pygame.transform.scale(quit_button_img, (200, 100))

def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

class Game:
    def __init__(self):
        self.pause_button_img = pygame.image.load('data/images/pause_buttons/pausebutton.png').convert_alpha()
        self.pause_button_img = pygame.transform.scale(self.pause_button_img, (70, 70))
        self.pause_button_rect = self.pause_button_img.get_rect(topleft=(20, 10))

        self.game_over_img = pygame.image.load('data/images/gameover.png').convert_alpha()
        self.game_over_img = pygame.transform.scale(self.game_over_img, (1366, 768))
        
        self.screen = screen
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))

        self.pixelatedfont = pygame.font.Font('data/fonts/pixelated.ttf', 40)

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False] 

        #Willie
        self.willie_start_x = -70
        self.willie_speed = 0.5
        self.willie_fixed_y = 10


        #Game Joystick
        pygame.joystick.init()
        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()


        self.elapsed_time = 0
        self.timer_duration = 7200 #1800 frames = 30 seconds at 60 FPS


        

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
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
        
        #load all sounds
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }
        
        #Set volume for all sounds
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
    
        self.screenshake = 0

        self.vid = Video('data/group7intro.mp4')
        self.vid.set_size((1366, 768))

        # Load tutorial images
        self.tutorial_images = [
            pygame.image.load('data/images/tutorial1.png').convert_alpha(),
            pygame.image.load('data/images/tutorial2.png').convert_alpha(),
            pygame.image.load('data/images/tutorial3.png').convert_alpha(),
            pygame.image.load('data/images/tutorial4.png').convert_alpha()
        ]

        #background image loading for all levels
        self.background_images = {
            0: 'data/images/levelbackground/background0.png',
            1: 'data/images/levelbackground/background1.png',
            2: 'data/images/levelbackground/background2.png',
        }

        self.level = 0
        self.load_level(self.level)
        
        self.is_jumping = False

        #all willie related content
        self.willie_face = pygame.image.load('data/willies/willie.png').convert_alpha()
        self.willie_face = pygame.transform.scale(self.willie_face, (self.willie_face.get_width(), 170))
        self.willie_jump_face = pygame.image.load('data/willies/williejump.png').convert_alpha()
        self.willie_jump_face = pygame.transform.scale(self.willie_jump_face, (self.willie_jump_face.get_width(), 170))
        self.reset_willie()
        self.prev_willie_y = self.willie_fixed_y
        
        self.start_time = pygame.time.get_ticks()
        self.total_start_time = self.start_time

        self.scores = self.load_scores()
        self.start_time = pygame.time.get_ticks()


    # Pause Menu
    def pause_menu(self, screen, clock):
        paused = True

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 20)) 

        resume_button_img = pygame.transform.scale(pygame.image.load('data/images/pause_buttons/resumebutton.png').convert_alpha(), (300, 100))
        quit_button_img = pygame.transform.scale(pygame.image.load('data/images/pause_buttons/quitbutton.png').convert_alpha(), (300, 100))
        credits_button_img = pygame.transform.scale(pygame.image.load('data/images/pause_buttons/creditsbutton.png').convert_alpha(), (300, 100))
        scores_button_img = pygame.transform.scale(pygame.image.load('data/images/pause_buttons/scoresbutton.png').convert_alpha(), (300, 100))
        
        resume_button_rect = resume_button_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 150))
        quit_button_rect = quit_button_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))
        scores_button_rect = scores_button_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        credits_button_rect = credits_button_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50 ))
 

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if resume_button_rect.collidepoint(mouse_pos):
                        paused = False
                    if scores_button_rect.collidepoint(mouse_pos):
                        self.display_scores()
                    if credits_button_rect.collidepoint(mouse_pos):
                        self.credit_screen()
                    if quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            screen.blit(overlay, (0, 0))

            # Draw buttons
            screen.blit(resume_button_img, resume_button_rect.topleft)
            screen.blit(credits_button_img, credits_button_rect.topleft)
            screen.blit(scores_button_img, scores_button_rect.topleft)
            screen.blit(quit_button_img, quit_button_rect.topleft)

            pygame.display.update()
            clock.tick(60)
        

    # Loading the levels
    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 3
            else:
                enemy_y = spawner['pos'][1] - 500
                self.enemies.append(Enemy(self, (spawner['pos'][0], enemy_y), (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

        if map_id in self.background_images:
            self.assets['background'] = pygame.image.load(self.background_images[map_id]).convert_alpha()
        else:
            self.assets['background'] = pygame.image.load('data/images/background.png').convert_alpha()

        if map_id == 2:
            self.willie_speed = 0.6

        #Conditions when the levels is finished
        if map_id == 3:
            self.display_image_and_wait('data/images/submit.png')
            self.update_scores()
            self.display_scores()
            self.winner_screen()  

        self.reset_willie()

        self.start_time = pygame.time.get_ticks()

    #Score System
    def load_scores(self):
        try:
            with open('data/scores.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_scores(self):
        with open('data/scores.json', 'w') as f:
            json.dump(self.scores, f)

    #Super duper COOL intro video
    def play_intro_video(self):
        self.vid.restart()
        while self.vid.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.vid.active = False

            self.screen.fill((0, 0, 0))
            self.vid.draw(self.screen, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
        self.vid.close()

    def reset_willie(self):
        self.willie_x = self.willie_start_x
        self.willie_fixed_y = 0 
    
    #display the tutorials for movements, attack and stuff
    def display_tutorial(self):
        for img in self.tutorial_images:
            displaying = True
            while displaying:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        displaying = False

                self.screen.fill((0, 0, 0))
                self.screen.blit(img, (0, 0))
                pygame.display.update()
                self.clock.tick(60)
        
    #Run 
    def run(self, clock):
        self.play_intro_video()  # Play the video once at the start
        self.display_tutorial()  # Display the tutorial images

        pygame.mixer.music.load('data/music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        
        self.sfx['ambience'].play(-1)
        
        while True:
            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(self.assets['background'], (0, 0))
            
            self.screenshake = max(0, self.screenshake - 1)
            self.willie_x += self.willie_speed
            self.elapsed_time += 1

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
            
            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] = (self.player.rect().centery - self.display.get_height() / 2) - 40
            
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
            
            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)


            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
                
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
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
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)
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
                    
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)
            
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)
            
            self.screen.fill((0, 0, 0))

            #willie logic
            willie_render_x = self.willie_x - 70
            self.willie_x += self.willie_speed
            self.prev_player_y = self.player.pos[1]

            if self.willie_x >= self.player.rect().centerx:
                self.dead = True
                self.load_level(self.level)


            if self.is_jumping:
                self.display.blit(self.willie_jump_face, (willie_render_x - self.scroll[0], self.willie_fixed_y))
            else:
                self.display.blit(self.willie_face, (willie_render_x - self.scroll[0], self.willie_fixed_y))

            


            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu(self.screen, self.clock)
                    elif event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    elif event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    elif event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sfx['jump'].play()
                            self.is_jumping = True
                    elif event.key == pygame.K_x:
                        self.player.dash()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    elif event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    elif event.key == pygame.K_UP:
                        self.is_jumping = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_rect.collidepoint(event.pos):
                        self.pause_menu(self.screen, self.clock)
                        
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        self.player.jump()
                        self.sfx['jump'].play()
                        self.is_jumping = True
                    elif event.button == 2:
                        self.player.dash()
                    elif event.button == 7:
                        self.pause_menu(self.screen, self.clock)

                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        self.is_jumping = False  # Set is_jumping to False when jump button released

                elif event.type == pygame.JOYHATMOTION:
                    hat_x, hat_y = event.value
                    if hat_x < 0:
                        self.movement[0] = True
                        self.movement[1] = False
                    elif hat_x > 0:
                        self.movement[0] = False
                        self.movement[1] = True
                    else:
                        self.movement[0] = False
                        self.movement[1] = False


            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            self.display_2.blit(self.display, (0, 0))
  
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
            self.screen.blit(self.pause_button_img, self.pause_button_rect.topleft)
            
            if self.elapsed_time >= self.timer_duration:
                self.game_over()

            self.render_timer()
            pygame.display.update()
            self.clock.tick(60)

    # Game over Function
    def game_over(self):
        font = self.pixelatedfont
        game_over_rect = self.game_over_img.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.game_over_img, game_over_rect)
            pygame.display.update()
            self.clock.tick(60)

    def display_image_and_wait(self, image_path):
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, (self.screen.get_width(), self.screen.get_height()))
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        waiting = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(image, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
    
    def render_timer(self):
        seconds = (self.timer_duration - self.elapsed_time) // 60
        minutes = seconds // 60
        seconds %= 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        stopwatch_text = f"{self.elapsed_time // 60:02d}:{self.elapsed_time % 60:02d}"
        text_color = pygame.Color('white')
        outline_color = pygame.Color('black')
        font = self.pixelatedfont

        # Render timer text
        outline_surface = font.render(timer_text, True, outline_color)
        text_surface = font.render(timer_text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 - 150, 30))
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            outline_rect = text_rect.move(dx, dy)
            self.screen.blit(outline_surface, outline_rect)
        self.screen.blit(text_surface, text_rect)

        # Render stopwatch text
        outline_surface = font.render(stopwatch_text, True, outline_color)
        text_surface = font.render(stopwatch_text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 170, 30))
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            outline_rect = text_rect.move(dx, dy)
            self.screen.blit(outline_surface, outline_rect)
        self.screen.blit(text_surface, text_rect)


    def winner_screen(self):
        font = self.pixelatedfont
        winner_text = "Special Thanks To Sir Willie (The boss) !"
        text_color = pygame.Color('white')
        outline_color = pygame.Color('black')
        text_surface = font.render(winner_text, True, text_color)
        outline_surface = font.render(winner_text, True, outline_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        video = Video('data/ending.mp4')
        video.set_size((self.screen.get_width(), self.screen.get_height()))
        video.restart()

        pygame.mixer.music.stop()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            self.screen.fill((0, 0, 0))

            if video.active:
                video.draw(self.screen, (0, 0))
                pygame.display.update()
                self.clock.tick(60)
            else:
                self.screen.blit(text_surface, text_rect)
                pygame.display.update()
                self.clock.tick(60)
                running = False

        video.close()
        thank_you_text = "Thank you Sir Willie"
        thank_you_surface = font.render(thank_you_text, True, text_color)
        thank_you_rect = thank_you_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))

            self.screen.blit(thank_you_surface, thank_you_rect)

            pygame.display.update()
            self.clock.tick(60)

    def reset_scores(self):
        self.scores = []
        self.save_scores()

    def credit_screen(self):
        credits = [
            "Group 7",
            "Leader : Iman Thaqif",
            "Game Design: Iman & Nazim",
            "Programming: Iman & Nazim",
            "Art: Iman & Nazim",
            "Music: Macroblank(YouTube) ",
            "Pygame Tutorial : 'DaFluffyPotato'(YouTube)",
        ]
        
        font = self.pixelatedfont
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False  

            self.screen.fill(BLACK)
            for i, line in enumerate(credits):
                draw_text(line, font, WHITE, self.screen, 100, 100 + i * 60)
            
            pygame.display.update()
            self.clock.tick(60)

    def update_scores(self):
        end_time = pygame.time.get_ticks()
        total_elapsed_time = (end_time - self.total_start_time) / 1000  # Total time in seconds
        self.scores.append(total_elapsed_time)
        self.scores = sorted(self.scores)[:10]  # Keep top 10 scores
        self.save_scores()


    def display_scores(self):
        font = self.pixelatedfont
        background_image = pygame.image.load('data/images/leaderboard.png').convert_alpha()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False  

            self.screen.fill(BLACK)
            self.screen.blit(background_image, (0, 0))  

            
            draw_text("Fastest Time", font, WHITE, self.screen, 200, 250)  

            for i, score in enumerate(self.scores):
                score_text = font.render(f"{i + 1}. {score:.2f} seconds", True, WHITE)
                self.screen.blit(score_text, (200, 300 + i * 60))  

            pygame.display.update()
            self.clock.tick(60)
    
Game().run(clock)
