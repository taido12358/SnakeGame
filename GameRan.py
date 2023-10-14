import pygame
from pygame import gfxdraw
from random import randrange
 
 
# Define Constants
 
BOARD_SIZE = 20  # Size of the board, in block
BLOCK_SIZE = 20  # Size of 1 block, in pixel
GAME_SPEED = 8  # Game speed (Normal = 10), The bigger, the faster
SIZE = (BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE) # 400 x 400
# Surface
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Python Snake")
score = 0
 
 
# ============================ THE SNAKE POSITION AND BEHAVIOUR ======
 
class Snake():
    def __init__(self):
        self.starting_position()
 
    def starting_position(self):
        "The coordinates of the start and direction are here"
 
        self.head = [
            # self.head[0] = x = 5
            int(BOARD_SIZE / 4),
            # self.head[1] = x = 5
            int(BOARD_SIZE / 4)]
        self.body = [[self.head[0], self.head[1]],
                     [self.head[0] - 1, self.head[1]],
                     [self.head[0] - 2, self.head[1]]
                     ]
        #   [ ][ ][ ] => right
        self.direction = "RIGHT"
        # Conditions to not go in the opposite direction
 
    def direction_to(self, direction):
        "When you hit a key in the while loop; avoid going backwards"
        opposites = [("RIGHT", "LEFT"),("UP", "DOWN")]
        for a, z  in opposites:
            if self.direction == a:
                if not direction == z:
                    self.direction = direction
                    break
            if self.direction == z:
                if not direction == a:
                    self.direction = direction
                    break
 
    def move(self, food_pos):
        moves = {
        "RIGHT": (0, 1),
        "LEFT": (0, -1),
        "UP" : (1, -1),
        "DOWN": (1, 1)
        }
        for k in moves:
            if self.direction == k:
                self.head[moves[k][0]] += moves[k][1]
 
        self.body.insert(0, list(self.head))
        if self.head == food_pos:
            return 1
        else:
            "If do not eat... same size"
            self.body.pop()
            return 0
 
    def check_collision(self):
        # Checks collision with border or himself
 
        conditions = (
            # x
            self.head[0] >= 20 or self.head[0] < 0,
            # y
            self.head[1] > 19 or self.head[1] < 0,
            # self
            [x for x in self.body[1:] if self.head == x]
        )
        if any(conditions):
            return 1
        else:
            return 0
 
# ============================= SPAWN FOOD =======================
 
class FoodSpawner():
    def __init__(self):
        self.food_pos = self.randompos()
        self.there_is_food = True
 
    def spawn_food(self):
        if self.there_is_food == False:
            self.food_pos = self.randompos()
            self.there_is_food = True
        return self.food_pos
 
    def set_food_on_screen(self, bool_value):
        self.there_is_food = bool_value
 
    def randompos(self):
        return [randrange(1, 20), randrange(1, 20)]
 
 
# ===================== DRAW HEAD, BODY and FOOD ================
 
class Draw:
    def draw_head(pos):
        pygame.draw.rect(
            window,
            (0, 255, 0),
            pygame.Rect(
                pos[0] * BLOCK_SIZE,
                pos[1] * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE))
 
    def draw_body(pos):
        pygame.draw.rect(window, (0, 128, 0), pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
 
    def delete_tail(pos):
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(snake.body[-1][0] * BLOCK_SIZE, snake.body[-1][1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
 
    def delete_fruit(pos, food_pos):
        x = food_pos[0] * BLOCK_SIZE + 10
        y = food_pos[1] * BLOCK_SIZE + 10
        r = 9
        gfxdraw.filled_circle(window, x, y, r, (0, 0, 0))
 
    def draw_fruit(food_pos):
        gfxdraw.filled_circle(window, food_pos[0] * BLOCK_SIZE + 10, food_pos[1] * BLOCK_SIZE + 10, 9, (255, 0, 0))
 
    def text_surface(text_to_show, x=0, y=0, middle="both"):
        "It write in the middle by default, if not middle='both' middle='x'"
        text = font.render(text_to_show, 1, pygame.Color("Coral"))
        if middle == "x":
            text_rect = text.get_rect(center=((SIZE[0] // 2, y)))
            window.blit(text, text_rect)      
        elif middle == "both":
            text_rect = text.get_rect(center=((SIZE[0] // 2, SIZE[1] // 2)))
            window.blit(text, text_rect)
        else:
            window.blit(text, (x, y))
        pygame.display.update()
 
 
# ================================= MANAGE GAME PART =================
 
class Game:
    clock = pygame.time.Clock()
    
    def restart():
        global GAME_SPEED
 
        GAME_SPEED = 8
        window.fill((0, 0, 0))
        snake.starting_position()
        Game.start()
 
 
    def press_to_start():
        "Initial menu"
        global loop, snake, food
        global font, size
 
        pygame.init()
        font = pygame.font.SysFont("Arial", 24)
        snake = Snake()
        food = FoodSpawner()
        Draw.text_surface("Python vs Snake", y=30, middle="x")
        Draw.text_surface("Press s to start")
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                loop = 0
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                    break
                if event.key == pygame.K_s:
                    Game.restart()
                    break
        pygame.quit()
 
 
    def start():
        global GAME_SPEED, score, loop
 
        food_pos = food.spawn_food()
        loop = 1
        while loop:
            if pygame.event.get(pygame.QUIT):
                loop = 0
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                loop = 0
            if keys[pygame.K_UP]:
                snake.direction_to("UP")
            if keys[pygame.K_DOWN]:
                snake.direction_to("DOWN")
            if keys[pygame.K_RIGHT]:
                snake.direction_to("RIGHT")
            if keys[pygame.K_LEFT]:
                snake.direction_to("LEFT")
            if snake.move(food_pos) == 1:
                # delete_fruit(pos, food_pos)
                score += 1
                food.set_food_on_screen(False)
                GAME_SPEED += 1
                food_pos = food.spawn_food()
 
            head = 1
            for pos in snake.body:
                if head == 1:
                    Draw.draw_head(pos)
                    head = 0
                else:
                    Draw.draw_body(pos)
            Draw.delete_tail(pos)
            Draw.draw_fruit(food_pos)
 
            if snake.check_collision() == 1:
                loop = 0
                Game.press_to_start()
            pygame.display.update()
            Game.clock.tick(GAME_SPEED)
 
        pygame.quit()
 
Game.press_to_start()