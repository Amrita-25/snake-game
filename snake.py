import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 0, 0)

# Fonts
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)


# ---------------- HIGH SCORE ----------------

HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


# ---------------- FOOD ----------------

def create_food(snake):
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        food = (x, y)

        if food not in snake:
            return food


# ---------------- NEW GAME ----------------

def new_game():
    snake = [
        (300, 300),
        (280, 300),
        (260, 300)
    ]

    direction = (CELL_SIZE, 0)
    food = create_food(snake)
    score = 0

    return snake, direction, food, score


# ---------------- DRAW GAME ----------------

def draw_game(snake, food, score, high_score):

    # Background
    screen.fill(BLACK)

    # Draw food
    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
    )

    # Draw snake
    for i, part in enumerate(snake):

        if i == 0:
            # Snake head
            color = GREEN
        else:
            # Snake body
            color = DARK_GREEN

        pygame.draw.rect(
            screen,
            color,
            (part[0], part[1], CELL_SIZE, CELL_SIZE)
        )

    # Display score
    score_text = font.render(
        f"Score: {score}   High Score: {high_score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))

    pygame.display.update()


# ---------------- GAME OVER SCREEN ----------------

def game_over_screen(score, high_score):

    screen.fill(BLACK)

    game_over_text = big_font.render(
        "GAME OVER",
        True,
        RED
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    high_score_text = font.render(
        f"High Score: {high_score}",
        True,
        WHITE
    )

    restart_text = font.render(
        "Press R to Restart",
        True,
        WHITE
    )

    screen.blit(
        game_over_text,
        (
            WIDTH // 2 - game_over_text.get_width() // 2,
            180
        )
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 - score_text.get_width() // 2,
            260
        )
    )

    screen.blit(
        high_score_text,
        (
            WIDTH // 2 - high_score_text.get_width() // 2,
            300
        )
    )

    screen.blit(
        restart_text,
        (
            WIDTH // 2 - restart_text.get_width() // 2,
            360
        )
    )

    pygame.display.update()


# ---------------- MAIN GAME ----------------

high_score = load_high_score()

snake, direction, food, score = new_game()

game_over = False
running = True


while running:

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Move up
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)

            # Move down
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)

            # Move left
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)

            # Move right
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)

            # Restart game
            elif event.key == pygame.K_r and game_over:

                snake, direction, food, score = new_game()
                game_over = False

    # ---------------- GAME LOGIC ----------------

    if not game_over:

        # Get current head position
        head_x, head_y = snake[0]

        # Calculate new head position
        new_head = (
            head_x + direction[0],
            head_y + direction[1]
        )

        # Check wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            game_over = True

        # Check collision with snake's body
        elif new_head in snake:
            game_over = True

        else:

            # Add new head
            snake.insert(0, new_head)

            # Check if snake ate food
            if new_head == food:

                score += 1

                # Update high score
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)

                # Create new food
                food = create_food(snake)

            else:

                # Remove tail
                snake.pop()

    # ---------------- DISPLAY ----------------

    if game_over:
        game_over_screen(score, high_score)
    else:
        draw_game(snake, food, score, high_score)

    # Control game speed
    clock.tick(10)


pygame.quit()