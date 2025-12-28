import pygame

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1280, 720
GRAVITY = 0.5
PLAYER_SPEED = 5
BASE_JUMP_POWER = -10
RUN_JUMP_BOOST = -5  
ANIMATION_DELAY = 5


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario")


background = pygame.image.load("background.jpg").convert()
ground = pygame.image.load("ground.png").convert()


background = pygame.transform.scale(background, (WIDTH, HEIGHT))
ground = pygame.transform.scale(ground, (WIDTH, 100))

ground_y = HEIGHT - 100


camera_x = 0


player_sprites_right = [
    pygame.image.load("mario_frame_0_transparent.png").convert_alpha(),
    pygame.image.load("mario_frame_1_transparent.png").convert_alpha(),
    pygame.image.load("mario_frame_2_transparent.png").convert_alpha(),
    pygame.image.load("mario_frame_4_transparent.png").convert_alpha()
]

player_sprites_left = [
    pygame.image.load("mario_frame_0_flipped.png").convert_alpha(),
    pygame.image.load("mario_frame_1_flipped.png").convert_alpha(),
    pygame.image.load("mario_frame_2_flipped.png").convert_alpha(),
    pygame.image.load("mario_frame_4_flipped.png").convert_alpha()
]


jump_sound = pygame.mixer.Sound("jump.wav")
horror_whisper = pygame.mixer.Sound("horror_whisper.wav")
background_music = pygame.mixer.Sound("background_music.wav")


pygame.mixer.Sound.play(background_music, loops=-1)


platforms = [
    pygame.Rect(0, ground_y - 80, WIDTH * 3, 20),
]


def draw_background():
    screen.blit(background, (camera_x % WIDTH - WIDTH, 0))
    screen.blit(background, (camera_x % WIDTH, 0))
    screen.blit(ground, (camera_x % WIDTH - WIDTH, ground_y))
    screen.blit(ground, (camera_x % WIDTH, ground_y))


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.frame = 0
        self.counter = 0
        self.facing_right = True

    def move(self):
        global camera_x
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        for platform in platforms:
            if self.rect.colliderect(platform) and self.vel_y > 0:
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True
                break
        else:
            self.on_ground = False

        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False

        if self.vel_x != 0:
            camera_x -= self.vel_x
            self.counter += 1
            if self.counter >= ANIMATION_DELAY:
                self.counter = 0
                self.frame = (self.frame + 1) % len(player_sprites_right)

    def jump(self):
        if self.on_ground:
            jump_power = BASE_JUMP_POWER + (RUN_JUMP_BOOST if abs(self.vel_x) > 0 else 0)
            self.vel_y = jump_power
            pygame.mixer.Sound.play(jump_sound)

    def draw(self, screen):
        if self.facing_right:
            screen.blit(player_sprites_right[self.frame], (self.rect.x, self.rect.y))
        else:
            screen.blit(player_sprites_left[self.frame], (self.rect.x, self.rect.y))


def draw_chat(screen, text, font, position=(50, HEIGHT - 130), box_width=WIDTH - 100, box_height=100):
    # Рисуем фон чата
    pygame.draw.rect(screen, (0, 0, 0), (position[0], position[1], box_width, box_height))
    pygame.draw.rect(screen, (255, 255, 255), (position[0], position[1], box_width, box_height), 3)


    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if font.size(current_line + word)[0] < box_width - 20:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())

    
    y_offset = position[1] + 10
    for line in lines:
        rendered_text = font.render(line, True, (255, 255, 255))
        screen.blit(rendered_text, (position[0] + 10, y_offset))
        y_offset += font.get_height()

font = pygame.font.Font(None, 36)
chat_texts = [
    "Привет! Как дела? Можешь помочь? Я ищу друга...",
    "Но знаешь, что странно?.. Сегодня утром мне показалось, что я слышал его голос... где-то далеко... но когда я обернулся, никого не было.",
    "И теперь у меня ощущение, что кто-то наблюдает за мной. Я не знаю, что происходит... но я должен его найти."
]
current_chat = 0
chat_active = True


running = True
clock = pygame.time.Clock()
player = Player(WIDTH // 4, 500)
while running:
    screen.fill((0, 0, 0))
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_c:
                chat_active = not chat_active
            if event.key == pygame.K_RETURN and chat_active:
                current_chat += 1
                if current_chat == 1:
                    pygame.mixer.Sound.set_volume(background_music, 0.2)
                    pygame.mixer.Sound.play(horror_whisper)
                elif current_chat >= len(chat_texts):
                    chat_active = False

    keys = pygame.key.get_pressed()
    player.vel_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED

    player.move()
    player.draw(screen)

    if chat_active and current_chat < len(chat_texts):
        draw_chat(screen, chat_texts[current_chat], font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()







