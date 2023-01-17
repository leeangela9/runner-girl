import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #walk images
        player_walk_1 = pygame.image.load('graphics/01.png').convert_alpha()
        player_walk_1 = pygame.transform.scale(player_walk_1, (80,90))
        player_walk_2 = pygame.image.load('graphics/02.png').convert_alpha()
        player_walk_2 = pygame.transform.scale(player_walk_2, (80,90))
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 #use to alternate player surfaces

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        #jump image + sound
        self.player_jump = pygame.image.load('graphics/jump.png').convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (80,90))

        self.jump_sound = pygame.mixer.Sound('audio/jump sound.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -22
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        #bird images
        if type == 'bird':
            bird_1 = pygame.image.load('graphics/bird1.png').convert_alpha()
            bird_1 = pygame.transform.scale(bird_1, (50,40))
            bird_2 = pygame.image.load('graphics/bird2.png').convert_alpha()
            bird_2 = pygame.transform.scale(bird_2, (50,40))
            self.frames = [bird_1, bird_2]
            y_pos = 210
        
        #dino images
        else:
            dino_1 = pygame.image.load('graphics/dino1.png').convert_alpha()
            dino_1 = pygame.transform.scale(dino_1, (60, 65))
            dino_2 = pygame.image.load('graphics/dino2.png').convert_alpha()
            dino_2 = pygame.transform.scale(dino_2, (60, 65))
            self.frames = [dino_1, dino_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def obstacle_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]  

    def update(self):
        self.obstacle_animation() 
        self.rect.x -= 6 + (0.01 * score)
        self.destroy()
            
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, '#efe9ff')
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init() #initalize pygame
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 60)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/first date.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#background:

sky_surf = pygame.image.load('graphics/sky1.jpeg').convert()
sky_surf = pygame.transform.scale(sky_surf, (800, 500))

ground_surf = pygame.image.load('graphics/grass.jpeg').convert() 
ground_surf = pygame.transform.scale(ground_surf, (800, 100))

#inital screen
player_stand = pygame.image.load('graphics/girl.gif').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (200,200))
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('running girl', False, '#e5a2bd')
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,340))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

#event handler
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #opp of init
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bird', 'dino', 'dino', 'dino', 'bird'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    #display
    if game_active:

        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
            
    else: #menu screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_msg = test_font.render(f'Your score: {score}', False, '#e5a2bd')
        score_msg_rect = score_msg.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_msg, score_msg_rect)

    pygame.display.update() #updates screen
    clock.tick(60)