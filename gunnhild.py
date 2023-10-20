import pygame, sys, random
from button import Button


class Coin(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if type == "beer":
            beer_surf = pygame.transform.scale2x(
                pygame.image.load("sprites/beer.png")
            ).convert_alpha()
            self.frames = [beer_surf]
        else:
            shot_surf = pygame.transform.scale2x(
                pygame.image.load("sprites/shot.png")
            ).convert_alpha()
            self.frames = [shot_surf]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midtop=(700, random.randint(200, 700)))

    def update(self):
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def draw_floor():
    screen.blit(floor_surf, (floor_x_pos, 900))
    screen.blit(floor_surf, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surf.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surf.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surf, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surf, False, True)
            screen.blit(flip_pipe, pipe)


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


def score_display(game_state):
    if game_state == "main_game":
        beer_score_surf = game_font.render(
            f"Slurker: {(int(beer_score))}", True, (255, 255, 255)
        )
        beer_score_rect = beer_score_surf.get_rect(center=(288, 100))
        shot_score_surf = game_font.render(
            f"Shots: {(int(shot_score))}", True, (255, 255, 255)
        )
        shot_score_rect = shot_score_surf.get_rect(center=(288, 200))
        screen.blit(beer_score_surf, beer_score_rect)
        screen.blit(shot_score_surf, shot_score_rect)
    if game_state == "game_over":
        beer_score_surf = game_font.render(
            f"{character_labels[selected_character_index]} må drikke {int(beer_score)} slurker",
            True,
            (255, 255, 255),
        )
        beer_score_rect = beer_score_surf.get_rect(center=(288, 100))
        shot_score_surf = game_font.render(
            f"{character_labels[selected_character_index]} må ta {int(shot_score)} shotter",
            True,
            (255, 255, 255),
        )
        shot_score_rect = shot_score_surf.get_rect(center=(288, 200))
        screen.blit(beer_score_surf, beer_score_rect)
        screen.blit(shot_score_surf, shot_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def coin_score_check():
    global beer_score, shot_score
    collided_sprites = [
        sprite for sprite in drank_group if player_rect.colliderect(sprite.rect)
    ]
    for collided_sprite in collided_sprites:
        if collided_sprite.type == "beer":
            beer_score += 1
            score_sound.play()
        else:
            shot_score += 1
            score_sound.play()

        drank_group.remove(collided_sprite)


pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)  # Use the correct index for your controller
controller.init()

screen = pygame.display.set_mode((576, 1024))
pygame.display.set_caption("Main menu")
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 40)

# Game variables
gravity = 0.25
player_movement = 0
game_active = True
beer_score = 0
shot_score = 0
high_score = 0
can_score = True

# Background
bg_surf = pygame.transform.scale2x(
    pygame.image.load("sprites/background-night.png")
).convert()

floor_surf = pygame.transform.scale2x(pygame.image.load("sprites/base.png")).convert()
floor_x_pos = 0

# Player animation
player_downflap = pygame.transform.scale2x(
    pygame.image.load("sprites/bluebird-downflap.png").convert_alpha()
)
"""
player_midflap = pygame.transform.scale2x(
    pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
)
player_upflap = pygame.transform.scale2x(
    pygame.image.load("sprites/bluebird-upflap.png").convert_alpha()
)
"""
# player_fames = [player_downflap, player_midflap, player_upflap]
player_index = 0
player_surf = player_downflap
player_rect = player_surf.get_rect(center=(100, 152))

PLAYERFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PLAYERFLAP, 200)

# Pipes / Obstacles
pipe_surf = pygame.image.load("sprites/pipe-green.png")
pipe_surf = pygame.transform.scale2x(pipe_surf)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# Coins / dranks
drank_group = pygame.sprite.Group()

beer_surf = pygame.image.load("sprites/beer.png")
beer_surf = pygame.transform.scale2x(beer_surf)
shot_surf = pygame.image.load("sprites/shot.png")
shot_surf = pygame.transform.scale2x(shot_surf)
SPAWNCOIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNCOIN, 1000)
coin_height = [300, 400, 500]

# Game over screen
game_over_surface = pygame.transform.scale2x(
    pygame.image.load("sprites/message.png").convert_alpha()
)
game_over_rect = game_over_surface.get_rect(center=(288, 512))

# Sounds
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100


# Define player character options
# nikken = pygame.image.load("sprites/nikken.png")

character_options = [
    "nikken.png",
    "tubis.png",
    "madsen.png",
    "knutsen.png",
    "myhre.png",
    "petter.png",
    "kvist.png",
    "carlos.png",
    "aleks.png",
    "oye.png",
]
character_labels = [
    "Nikken",
    "Tubis",
    "Pysa",
    "Casino",
    "Ståbukser",
    "Kjekkepetter",
    "Fittekongen",
    "Coach",
    "David",
    "Regnbuegutten",
]
selected_character_index = 0  # Initially, the first character is selected

# Load character images
character_images = [
    pygame.transform.scale(
        pygame.image.load(f"sprites/{char}"), (80, 80)
    ).convert_alpha()
    for char in character_options
]
player_surf = character_images[selected_character_index]


def get_font(size):
    return pygame.font.Font("fonts/font.ttf", size)


def play():
    global game_active, player_movement, player_surf, player_rect, pipe_list, floor_x_pos, player_index, beer_score, shot_score, high_score, selected_character_index

    pygame.display.set_caption("GÆTTA")

    while True:
        for event in pygame.event.get():
            # Check for controller input
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    player_movement = 0
                    player_movement -= 10
                    flap_sound.play()

                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    player_rect.center = (100, 512)
                    player_movement = 0
                    beer_score = 0
                    shot_score = 0
                if event.key == pygame.K_UP and game_active == False:
                    select_player()

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

            if event.type == SPAWNCOIN:
                drank_group.add(Coin(random.choice(["beer", "shot"])))

            if event.type == PLAYERFLAP:
                if player_index < 2:
                    player_index += 1
                else:
                    player_index = 0
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                if button == 0 and game_active:
                    player_movement = 0
                    player_movement -= 10
                    flap_sound.play()
                if button == 0 and not game_active:
                    game_active = True
                    pipe_list.clear()
                    player_rect.center = (100, 512)
                    player_movement = 0
                    beer_score = 0
                    shot_score = 0
                if button == 1 and not game_active:
                    select_player()
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
            drank_group.draw(screen)
            drank_group.update()

            # Score
            coin_score_check()
            score_display("main_game")

        else:
            screen.blit(game_over_surface, game_over_rect)
            score_display("game_over")

        # Floor
        draw_floor()
        floor_x_pos -= 1

        if floor_x_pos <= -576:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120)


def select_player():
    global player_surf, selected_character_index

    pygame.display.set_caption("Velg spiller")

    # Initialize variables for character selection
    selected_character_index = 0
    character_x = 125
    character_y = 275

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        OPTIONS_TEXT = get_font(30).render("Velg spiller", True, "Red")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 150))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Define the positions of your menu items
        menu_items = [(OPTIONS_RECT.centerx, 800)] + [
            (character_x, character_y) for _ in range(len(character_images))
        ]
        # Display character options
        character_x = 125
        character_y = 275
        for i, char_image in enumerate(character_images):
            char_rect = char_image.get_rect(center=(character_x, character_y))
            screen.blit(char_image, char_rect)

            # Display the character label below the character image
            label_text = get_font(15).render(character_labels[i], True, "White")
            label_rect = label_text.get_rect(center=(character_x, character_y + 60))
            screen.blit(label_text, label_rect)

            if i == selected_character_index:
                pygame.draw.rect(
                    screen, (0, 255, 0), char_rect, 2
                )  # Highlight the selected character
            character_x += 175
            if character_x >= 576:
                character_x = 125
                character_y += 130

        PLAY_BUTTON = Button(
            image=None,
            pos=(300, 800),
            text_input="KJØR",
            font=get_font(30),
            base_color="Yellow",
            hovering_color="Pink",
        )

        PLAY_BUTTON.change_color(OPTIONS_MOUSE_POS)
        PLAY_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(OPTIONS_MOUSE_POS):
                    play()

                # Check for clicks on character options
                character_x = 125
                character_y = 275
                for i in range(len(character_images)):
                    char_rect = character_images[i].get_rect(
                        center=(character_x, character_y)
                    )
                    if char_rect.collidepoint(OPTIONS_MOUSE_POS):
                        selected_character_index = i
                        player_surf = character_images[selected_character_index]
                    character_x += 175
                    if character_x >= 576:
                        character_x = 125
                        character_y += 130
            
            # Handle controller input
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                if button == 14:  # Replace with the button number for moving down
                    selected_character_index = (selected_character_index + 1) % len(
                        character_images
                    )
                elif button == 13:  # Replace with the button number for moving up
                    selected_character_index = (selected_character_index - 1) % len(
                        character_images
                    )
                elif (
                    button == 11
                ):  # Replace with the button number for confirming the selection
                    selected_character_index = (selected_character_index - 3) % len(
                        character_images
                    )
                elif button == 12:
                    selected_character_index = (selected_character_index + 3) % len(
                        character_images
                    )

                elif button == 0:
                    # This is the "KJØR" button, trigger the play function
                    play()
                # Handle character selection
                player_surf = character_images[selected_character_index]

        OPTIONS_MOUSE_POS = menu_items[
            selected_character_index
        ]  # Update the mouse position based on the selection

        pygame.display.update()


def main_menu():
    pygame.display.set_caption("Menu")
    # Define the buttons and their positions
    # Initialize selected button index
    selected_button_index = 0

    while True:
        screen.blit(bg_surf, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("FLAPPY GUNNHILD", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 200))

        PLAY_BUTTON = Button(
            image=None,
            pos=(300, 350),
            text_input="PLAY",
            font=get_font(30),
            base_color="White",
            hovering_color="yellow",
        )
        OPTIONS_BUTTON = Button(
            image=None,
            pos=(300, 500),
            text_input="VELG SPILLER",
            font=get_font(30),
            base_color="White",
            hovering_color="green",
        )
        QUIT_BUTTON = Button(
            image=None,
            pos=(300, 650),
            text_input="QUIT",
            font=get_font(30),
            base_color="White",
            hovering_color="green",
        )

        screen.blit(MENU_TEXT, MENU_RECT)

        buttons = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]

        for button in buttons:
            x = buttons[selected_button_index].x_pos
            y = buttons[selected_button_index].y_pos
            button.change_color((x,y))
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.check_for_input(MENU_MOUSE_POS):
                    select_player()
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                if button == 11:
                    selected_button_index = (selected_button_index - 1) % len(
                        buttons
                    )  # Move up
                    print(selected_button_index)
                elif button == 12:
                    print("down")
                    selected_button_index = (selected_button_index + 1) % len(
                        buttons
                    )  # Move down
                elif button == 0:
                    if selected_button_index == 0:
                        play()
                    elif selected_button_index == 1:
                        select_player()
                    elif selected_button_index == 2:
                        pygame.quit()
                        sys.exit()

            # Render buttons and highlight the selected button
            for i, button in enumerate(buttons):
                if i == selected_button_index:
                    button.change_color((x,y))
                else:
                    button.change_color((x,y))
                button.update(screen)
                pygame.display.update()


main_menu()
