import pygame
import os

pygame.init()
pygame.font.init()

FPS = 60
VEL = 5
WIDTH, HEIGHT = 800, 600
BORDER_THIN = 5
MAX_BULLET_SPEED = 7
MAX_BULLET = 3

PLAYER_HIT = pygame.USEREVENT + 1
OPPONENT_HIT = pygame.USEREVENT + 2

# BOTH BULLETS  HIT SIMULTANEOUSLY

BULLETS_COLLIDE = pygame.USEREVENT + 3


HEALTH_FONT = pygame.font.SysFont("Arial",25,bold=True)

PLAYER_ON_X_AXIS, PLAYER_ON_Y_AXIS = 400, 475
OPPONENT_ON_X_AXIS,OPPONENT_ON_Y_AXIS = 400, 40

# TEXT FONT FOR WINNERS
WINNER_FONT = pygame.font.SysFont("comicsans", 40)


WHITE = (255, 255, 255)
BORDER = pygame.Rect(0, HEIGHT / 2, WIDTH, BORDER_THIN)
PLAYER_SHIP_WIDTH, PLAYER_SHIP_HEIGHT = 70, 70
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")\
    
SPACE = pygame.image.load(os.path.join("images", "space_3.png"))
PLAYER_SHIP_IMAGE = pygame.image.load(os.path.join('images', 'player_ship.png'))
PLAYER_SHIP = pygame.transform.scale(PLAYER_SHIP_IMAGE, (PLAYER_SHIP_WIDTH, PLAYER_SHIP_HEIGHT))

OPPONENT_SHIP_IMAGE = pygame.image.load(os.path.join('images', 'opponent_ship.png'))
OPPONENT_SHIP = pygame.transform.rotate(pygame.transform.scale(OPPONENT_SHIP_IMAGE,
                                                               (PLAYER_SHIP_WIDTH, PLAYER_SHIP_HEIGHT)), 180)
# LOGO
pygame.display.set_icon(pygame.image.load(os.path.join('images', 'player_ship.png')))

def draw_winner(text):
    text_winner = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(text_winner, (WIDTH / 2 - text_winner.get_width() / 2, HEIGHT / 2 - text_winner.get_height()))
    pygame.display.update()
    pygame.time.delay(3000)


def draw(player, opponent, player_bullets, opponent_bullets, player_health, opponent_health):
    WIN.blit(SPACE, (0, 0))  # (25, 29, 30) space color
    pygame.draw.rect(WIN, (255, 255, 0), BORDER)

    WIN.blit(PLAYER_SHIP, (player.x, player.y))
    WIN.blit(OPPONENT_SHIP, (opponent.x, opponent.y))

    player_health_text = HEALTH_FONT.render("HEALTH: " + str(player_health), True, WHITE)
    opponent_health_text = HEALTH_FONT.render("HEALTH: " + str(opponent_health), True, WHITE)

    WIN.blit(player_health_text, (WIDTH - player_health_text.get_width() - 10, 8))
    WIN.blit(opponent_health_text, (WIDTH - opponent_health_text.get_width() - 10, HEIGHT - 50))

    for bullet in player_bullets:
        pygame.draw.rect(WIN, (255, 0, 0), bullet)
    for bullet in opponent_bullets:
        pygame.draw.rect(WIN, (0, 0, 255), bullet)

    #pygame.draw.rect(WIN, (255, 0, 0), opponent.x, opponent.y + 20, 50, 10)
    pygame.display.update()

def player_moves(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x - VEL > 0:  # MOVE TOWARDS LEFT
        player.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and player.x + VEL + player.width < WIDTH:  # MOVE TOWARDS RIGHT
        player.x += VEL
    if keys_pressed[pygame.K_UP] and player.y - VEL > BORDER.y + 5:  # MOVE TOWARDS UP
        player.y -= VEL
    if keys_pressed[pygame.K_DOWN] and player.y + VEL + player.height < HEIGHT:  # MOVE TOWARDS DOWN
        player.y += VEL

'''def collide_bullets(bullets, player_bullets, opponent_bullets):
    if bullets.colliderect(bullets):
        pygame.event.post(pygame.event.Event(BULLETS_COLLIDE))
        player_bullets.remove(bullets)
        opponent_bullets.remove(bullets)'''

def opponent_moves(keys_pressed, opponent):
    if keys_pressed[pygame.K_a] and opponent.x - VEL > 0:  # MOVE TOWARDS LEFT
        opponent.x -= VEL
    if keys_pressed[pygame.K_d] and opponent.x + VEL + opponent.width < WIDTH:  # MOVE TOWARDS RIGHT
        opponent.x += VEL
    if keys_pressed[pygame.K_w] and opponent.y - VEL > 0:  # MOVE TOWARDS UP
        opponent.y -= VEL
    if keys_pressed[pygame.K_s] and opponent.y + VEL + opponent.height < BORDER.y:  # MOVE TOWARDS DOWN
        opponent.y += VEL

def handle_bullets(player_bullets, opponent_bullets, player, opponent):
    for bullet in player_bullets:
        bullet.y -= MAX_BULLET_SPEED
        if opponent.colliderect(bullet):
            pygame.event.post(pygame.event.Event(OPPONENT_HIT))
            player_bullets.remove(bullet)
        elif bullet.y <= 0:
            player_bullets.remove(bullet)
    for bullet in opponent_bullets:
        bullet.y += MAX_BULLET_SPEED
        if player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            opponent_bullets.remove(bullet)
        elif bullet.y >= HEIGHT-10:
            opponent_bullets.remove(bullet)

def main():
    player = pygame.Rect(PLAYER_ON_X_AXIS, PLAYER_ON_Y_AXIS, PLAYER_SHIP_WIDTH, PLAYER_SHIP_HEIGHT)
    opponent = pygame.Rect(OPPONENT_ON_X_AXIS, OPPONENT_ON_Y_AXIS, PLAYER_SHIP_WIDTH, PLAYER_SHIP_HEIGHT)
    clock = pygame.time.Clock()

    player_health = 10
    opponent_health = 10

    player_bullets = []
    opponent_bullets = []

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(player_bullets) <= MAX_BULLET:
                    bullet = pygame.Rect(player.x + player.width // 2, player.y - player.height//4, 5, 10)
                    player_bullets.append(bullet)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(opponent_bullets) <= MAX_BULLET:
                    bullet = pygame.Rect(opponent.x + opponent.width // 2, opponent.y
                                         + opponent.height - opponent.height // 4, 5, 10)
                    opponent_bullets.append(bullet)

            if event.type == PLAYER_HIT and opponent_health >= 0:
                opponent_health_show = pygame.Rect(opponent.x, opponent.y-10, 10, 5)
                opponent_health -= 1

            if event.type == OPPONENT_HIT and player_health >= 0:
                player_health_show = pygame.Rect(player.x + 15, player.y + 40, 10, 5)
                player_health -= 1

        winner_text = ""
        if player_health <= 0:
            winner_text = "PLAYER WINS"
        if opponent_health <= 0:
            winner_text = "OPPONENT WINS"
        if winner_text != "":  # Show the winner on the screen
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        player_moves(keys_pressed, player)
        opponent_moves(keys_pressed, opponent)
        """for bullets in player_bullets, opponent_bullets:
            collide_bullets(bullets, player_bullets, opponent_bullets)"""

        handle_bullets(player_bullets, opponent_bullets, player, opponent)
        draw(player, opponent, player_bullets, opponent_bullets, player_health, opponent_health)

    main()

if __name__ == '__main__':
    main()
