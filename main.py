import pygame, sys, random
from button import Button

def draw_floor():
    screen.blit(floor_surf, (floor_x_pos, 900))
    screen.blit(floor_surf, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surf.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surf.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def create_coin():
    random_coin_height = random.choice(range(200,700))
    main_coin = coin_surf.get_rect(midtop=(700, random_coin_height))
    return main_coin


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def move_coin(coins):
    for coin in coins:
        coin.centerx -= 5
    visible_coins = [coin for coin in coins if coin.right > -50]
    return visible_coins


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surf, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surf, False, True)
            screen.blit(flip_pipe, pipe)


def draw_coins(coins):
    for coin in coins:
        screen.blit(coin_surf, coin)


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if player_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if player_rect.top <= -100 or player_rect.bottom >= 900:
        death_sound.play()
        can_score = True
        return False
    return True

def rotate_player(player):
    new_player = pygame.transform.rotozoom(player, -player_movement * 3, 1)
    return new_player


def player_animation():
    new_player = player_fames[player_index]
    new_player_rect = player_surf.get_rect(center=(100, player_rect.centery))
    return new_player, new_player_rect


def score_display(game_state):
    if game_state == "main_game":
        score_surf = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(288, 100))
        screen.blit(score_surf, score_rect)
    if game_state == "game_over":
        score_surf = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(288, 100))
        screen.blit(score_surf, score_rect)

        high_score_surf = game_font.render(
            f"Carlsberg: {int(high_score)}", True, (255, 255, 255)
        )
        score_rect = score_surf.get_rect(center=(288, 100))
        high_score_rect = score_surf.get_rect(center=(288, 850))
        screen.blit(high_score_surf, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score

    if coin_list:
        for coin in coin_list:
            if player_rect.colliderect(coin):
                score += 1
                score_sound.play()
                coin_list.remove(coin)

def character_selection_screen():
    global selected_character, character_selection

    screen.fill((0, 0, 0))
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Select Your Character", True, "white")
    screen.blit(title_text, (WIDTH // 2 - 150, 50))

    for i, character in enumerate(characters):
        character_img = pygame.image.load(character)
        x = (WIDTH // 2) - (len(characters) * 50) + i * 100
        y = HEIGHT // 2 - 24
        screen.blit(character_img, (x, y))
        if i == selected_character:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, 34, 24), 2)




pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("fonts/carlsberg.ttf", 40)


# Game variables
gravity = 0.25
player_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True


bg_surf = pygame.transform.scale2x(
    pygame.image.load("sprites/background-night.png")
).convert()

floor_surf = pygame.image.load("sprites/base.png").convert()
floor_surf = pygame.transform.scale2x(floor_surf)
floor_x_pos = 0


player_downflap = pygame.transform.scale2x(
    pygame.image.load("sprites/bluebird-downflap.png").convert_alpha()
)
player_midflap = pygame.transform.scale2x(
    pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
)
player_upflap = pygame.transform.scale2x(
    pygame.image.load("sprites/bluebird-upflap.png").convert_alpha()
)
player_fames = [player_downflap, player_midflap, player_upflap]
player_index = 0
player_surf = player_fames[player_index]
player_rect = player_surf.get_rect(center=(100, 152))

PLAYERFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PLAYERFLAP, 200)

# player_surf = pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
# player_surf = pygame.transform.scale2x(player_surf)
# player_rect = player_surf.get_rect(center = (100,512))


pipe_surf = pygame.image.load("sprites/pipe-green.png")
pipe_surf = pygame.transform.scale2x(pipe_surf)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]


coin_surf = pygame.image.load("sprites/beer.png")
coin_surf = pygame.transform.scale2x(coin_surf)
coin_list = []
SPAWNCOIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNCOIN, 1000)
coin_height = [300, 400, 500]


game_over_surface = pygame.transform.scale2x(
    pygame.image.load("sprites/message.png").convert_alpha()
)
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                player_movement = 0
                player_movement -= 12
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                coin_list.clear()
                player_rect.center = (100, 512)
                player_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == SPAWNCOIN:
            coin_list.append(create_coin())

        if event.type == PLAYERFLAP:
            if player_index < 2:
                player_index += 1
            else:
                player_index = 0

            player_surf, player_rect = player_animation()
    screen.blit(bg_surf, (0, 0))

    if game_active:
        # Player
        player_movement += gravity
        rotated_player = rotate_player(player_surf)
        player_rect.centery += player_movement
        screen.blit(rotated_player, player_rect)

        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Coins
        coin_list = move_coin(coin_list)
        draw_coins(coin_list)

        # Score
        pipe_score_check()
        score_display("main_game")

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    # Floor
    draw_floor()
    floor_x_pos -= 1
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)



if __name__ == "__main__":
    main()