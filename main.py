import pygame
import os

from colors import Color
from movements import Movement

# init font ans sound
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starship")
FPS = 60
VEL = 5
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 30, 30
BORDER = pygame.Rect(WIDTH // 2, 0, 10, HEIGHT)

# Bullets
BULLET_VEL = 7
MAX_BULLET = 3

# User Event
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# fonts
HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WINNNER_FONT = pygame.font.SysFont("comicsans", 100)

# sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Gun+Silencer.mp3"))


# First spaceship (yellow)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
)
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

# Second spaceship (red)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
)
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

SPACE_IMAGE = pygame.image.load("Assets\\space.png")
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    """
    handles bullets

    Add bullet to players bullet list
    """
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# Main Window
def draw_window(
    yellow, red, yellow_bullets, red_bullets, yellow_health, red_health
):
    """
    Draws main window
    """

    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, Color.black, BORDER)

    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, Color.white)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, Color.white)
    WIN.blit(yellow_health_text,
             (WIDTH - yellow_health_text.get_width() - 10, 10))
    WIN.blit(red_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, Color.yellow, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, Color.red, bullet)

    pygame.display.update()


def draw_winner(text):
    """
    Draws winner text
    """

    draw_text = WINNNER_FONT.render(text, 1, Color.white)
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    # players
    yellow = pygame.Rect(
        100, 50, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(
        800, 350, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # bullets list
    yellow_bullets = []
    red_bullets = []

    # health
    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            # To quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Handle bullets
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LCTRL and
                        len(yellow_bullets) < MAX_BULLET):
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if (event.key == pygame.K_RCTRL and
                        len(red_bullets) < MAX_BULLET):
                    bullet = pygame.Rect(
                        red.x + red.width,
                        red.y + red.height // 2 - 2,
                        10,
                        5
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # Handle Hit
            if event.type == YELLOW_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # Handle Winner
        winner = ""
        if yellow_health <= 0:
            winner = "Yello Wins!"

        if red_health <= 0:
            winner = "Red Wins!"

        if winner != "":
            draw_winner(winner)
            break

        # Handle player movements
        movement = Movement(height=HEIGHT, width=WIDTH,
                            velocity=VEL,  border=BORDER)
        key_pressed = pygame.key.get_pressed()
        movement.player1_handle_movement(
            player1=yellow, key_pressed=key_pressed)
        movement.player2_handle_movement(
            player2=red, key_pressed=key_pressed)

        handle_bullets(
            yellow_bullets, red_bullets, yellow, red)
        draw_window(yellow, red, yellow_bullets,
                    red_bullets, yellow_health, red_health)
    main()


if __name__ == "__main__":
    main()
