import psycopg2
import pygame
import sys
import random
import time
from pygame.math import Vector2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="suppliers",
        user="postgres",
        password="FALga814",
        connect_timeout=10,
        sslmode="prefer"
)

def create_high_scores_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS high_scores (
            id SERIAL PRIMARY KEY,
            player_name VARCHAR(50),
            apples_eaten INTEGER,
            game_level INTEGER  -- Добавлен новый столбец
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_score(name, apples_eaten, game_level):  # Изменено название параметра
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO high_scores (player_name, apples_eaten, game_level) VALUES (%s, %s, %s)", (name, apples_eaten, game_level))  # Изменено название столбца
    conn.commit()
    cur.close()
    conn.close()

def get_top_scores(limit=10):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT player_name, apples_eaten, game_level FROM high_scores ORDER BY apples_eaten DESC LIMIT %s", (limit,))  # Изменено название столбца
    scores = cur.fetchall()
    cur.close()
    conn.close()
    return scores

# Добавление имени
name = input("Введите имя: ")

class Fruit:
    def __init__(self):
        self.randomize()
        self.is_gold = False
        self.golden_time = 0

    # Метод для отрисовки яблока
    def draw_fruit(self):
        if self.is_gold:
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            screen.blit(sized_gold_apple, fruit_rect)
        else:
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            screen.blit(sized_apple, fruit_rect)
    
    # Случайное размещение яблока
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    # Инициализация
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # Первые три блока
        self.direction = Vector2(1, 0)  # Направление
        self.new_block = False

    # Отрисовка змеи
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)
    
    # Метод перемещения змеи
    def move_snake(self):
        if self.new_block:  # Если нужен новый блок
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:  # Остается таким же, просто перемещается
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        
    # Метод добавления блока в задний конец
    def add_block(self):
        self.new_block = True

class Main:
    # Инициализация
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.fruits_eaten = 0
        self.timer_interval = 150 
        self.level = 1

    # Метод обновления (перемещение змеи, проверка столкновения с яблоком и змеей, проверка, не выходит ли змея за границы)
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.check_golden_fruit_timeout()

    # Отрисовка элементов на экране
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_level()
        
    # Метод проверки столкновения
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            if self.fruit.is_gold:
                self.fruits_eaten += 5
            else:
                self.fruits_eaten += 1
            self.fruit.randomize()
            self.fruit.is_gold = random.choice([True, False])
            self.snake.add_block()
            if self.fruits_eaten % 4 == 0 and self.timer_interval >= 45:
                self.decrease_timer_interval()
                self.level += 1
            if random.choice([True, False]):
                self.fruit.is_gold = True
                self.fruit.golden_time = time.time()
            else:
                self.fruit.is_gold = False

    # Увеличение скорости путем уменьшения интервала таймера
    def decrease_timer_interval(self):
        self.timer_interval -= 15
        pygame.time.set_timer(SCREEN_UPDATE, self.timer_interval)
    
    # Проверка, не выходит ли змея за границы экрана
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    # Завершение игры
    def game_over(self):
        time.sleep(1.2)
        pygame.quit()
        insert_score(name, self.fruits_eaten, self.level)
        print(f"{name} съел {self.fruits_eaten} яблок на уровне {self.level}")
        sys.exit()
    
    # Отрисовка травяного узора, каждая нечетная клетка меняет цвет на цвет травы
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for column in range(cell_number):
                    if column % 2 == 1:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    # Отрисовка счета на экране
    def draw_score(self):
        score_text = str(self.fruits_eaten)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = sized_apple.get_rect(midright=(score_rect.left, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(sized_apple, apple_rect)

    # Отрисовка уровня на экране
    def draw_level(self):
        level_text = 'Level: ' + str(self.level)
        level_surface = game_font.render(level_text, True, (56, 74, 12))
        level_x = int(cell_size * cell_number - 60)
        level_y = int(cell_size * cell_number - 640)
        level_rect = level_surface.get_rect(center=(level_x, level_y))
        screen.blit(level_surface, level_rect)

    # 7 секунд для золотого яблока
    def check_golden_fruit_timeout(self):
        if self.fruit.is_gold and (time.time() - self.fruit.golden_time > 7):
            self.fruit.is_gold = False

    def draw_top_scores(self):
        top_scores = get_top_scores()
        y_offset = 30
        for score in top_scores:
            score_surface = game_font.render(f"{score[0]}: {score[1]}", True, (255, 255, 255))
            screen.blit(score_surface, (50, y_offset))
            y_offset += 30

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
fps = pygame.time.Clock()
apple = pygame.image.load('image/3263dbbe79bb3e1.png').convert_alpha()
golden = pygame.image.load('image/915-9155022_golden-apple-yoshis-island-yoshi-sprites.png').convert_alpha()
sized_apple = pygame.transform.scale(apple, (40, 40))
sized_gold_apple = pygame.transform.scale(golden, (40, 40))
game_font = pygame.font.Font(None, 40)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
main_game = Main()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
    
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    
    pygame.display.update()
    fps.tick(120)

if __name__ == "__main__":
    create_high_scores_table()
    pygame.init()
