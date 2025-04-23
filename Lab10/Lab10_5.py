import pygame, sys, random, time
from pygame.locals import *
import psycopg2

pygame.init()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
CELL_SIZE = 20
COLS = WINDOW_WIDTH // CELL_SIZE
ROWS = WINDOW_HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def connect_db():
    return psycopg2.connect(
        dbname="PhoneBook_DB",       
        user="postgres",       
        password="123456",   
        host="localhost",
        port="5432"
    )

def get_or_create_user(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM \"user\" WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        user_id = result[0]
        cur.execute("SELECT level, score FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
        data = cur.fetchone()
        level = data[0] if data else 1
        score = data[1] if data else 0
        print(f"Welcome back, {username}! Level: {level}, Score: {score}")
    else:
        cur.execute("INSERT INTO \"user\" (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        level = 1
        score = 0
        print(f"New user created: {username}")

    cur.close()
    conn.close()
    return user_id, level, score

def save_game(user_id, level, score):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s)", (user_id, level, score))
    conn.commit()
    cur.close()
    conn.close()
    print("Game saved!")


def generate_food(snake_body):
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) not in snake_body:
            food_type = random.choice([(RED, 10), (BLUE, 20), (YELLOW, 30)])
            return (x, y, food_type[0], food_type[1], time.time() + random.randint(5, 10))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game with Save & Pause")
clock = pygame.time.Clock()

username = input("Enter your username: ")
user_id, level, score = get_or_create_user(username)
speed = 3 + (level - 1) * 2
foods_eaten = 0

snake = [(COLS // 2, ROWS // 2)]
direction = (1, 0)
food = generate_food(snake)
running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused
            elif event.key == K_s:
                save_game(user_id, level, score)
            elif not paused:
                if event.key == K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

    if not paused:
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS or new_head in snake:
            running = False
            continue

        snake.insert(0, new_head)

        if time.time() > food[4]:
            food = generate_food(snake)

        if new_head[:2] == food[:2]:
            score += food[3]
            foods_eaten += 1
            food = generate_food(snake)
            if foods_eaten % 3 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

    screen.fill(BLACK)

    food_rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, food[2], food_rect)

    for segment in snake:
        seg_rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, seg_rect)

    font = pygame.font.SysFont("Verdana", 20)
    info_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(info_text, (10, 10))

    if paused:
        pause_text = pygame.font.SysFont("Verdana", 30).render("Paused", True, YELLOW)
        screen.blit(pause_text, (WINDOW_WIDTH//2 - 60, WINDOW_HEIGHT//2 - 20))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
sys.exit()
