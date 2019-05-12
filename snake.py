from sense_hat import SenseHat
from random import randint
from time import sleep
import copy

sense = SenseHat()
sense.clear()

r = (255,0,0)
g = (0, 255, 0)
ghead = (0, 128, 0)
b = (0,0,0)
w = (255,255,255)
game_over = False
score = 0

def calc_start_coords():
  prey_x = randint(0, 7)
  prey_y = randint(0, 7)
  snake_x = prey_x
  snake_y = prey_y
  while (prey_x == snake_x and prey_y == snake_y):
    snake_x = randint(0, 7)
    snake_y = randint(0, 7)
  return prey_x, prey_y, snake_x, snake_y

def place_new_prey(snake):
  prey_x = randint(0, 7)
  prey_y = randint(0, 7)
  while (snake.count([prey_x, prey_y]) > 0):
    prey_x = randint(0, 7)
    prey_y = randint(0, 7)
  return prey_x, prey_y

def move_snake(pitch, roll, x, y):
  new_x = x
  new_y = y
  if 1 < pitch < 179 and x != 0:
    new_x -= 1
  elif 359 > pitch > 179 and x != 7:
    new_x += 1
  if 1 < roll < 179 and y != 7:
    new_y += 1
  elif 359 > roll > 179 and y != 0:
    new_y -= 1
  
  if new_x != x and new_y != y:
    if pitch > roll:
      return new_x, y  
    elif pitch < roll:
      return x, new_y
  
  return new_x, new_y


def draw_board(snake):
  sense.clear()
  sense.set_pixel(prey_x, prey_y, r)
  for x in range(len(snake)):
    if x == 0:	# draw head
      sense.set_pixel(snake[x][0], snake[x][1], ghead)
    else:
      sense.set_pixel(snake[x][0], snake[x][1], g)
    
def check_win(x, y, snake):
  global game_over
  temp_snake = copy.deepcopy(snake)
  if len(temp_snake) > 4:
    for i in range(0, 3):
      temp_snake[i] = []
    if temp_snake.count([x, y]) > 0:
      print("found {:d} {:d}".format(x, y))
      game_over = True
      sense.show_message("{:d}".format(score))

prey_x, prey_y, snake_x, snake_y = calc_start_coords();
snake = [[snake_x, snake_y]]

while not game_over:
  o = sense.get_orientation()
  pitch = o['pitch']
  roll = o['roll']
  old_snake_x = snake_x
  old_snake_y = snake_y
  sense.set_pixel(snake_x, snake_y, b)
  snake_x, snake_y = move_snake(pitch, roll, snake_x, snake_y)
  print("coords: {:d} - {:d}".format(snake_x, snake_y))
  check_win(snake_x, snake_y, snake)

  #if coords already exist, do not insert it again!
  if snake.count([snake_x, snake_y]) > 0:
    snake_x = old_snake_x
    snake_y = old_snake_y
  else:
    temp_snake = []
    temp_snake.append([snake_x, snake_y])
    index = 0
    # maintain the sequence of snake body parts
    while len(temp_snake) < len(snake):
      temp_snake.append(snake[index])
      index += 1
    snake = temp_snake

  # prey has been eaten
  if snake_x == prey_x and snake_y == prey_y:
    snake.append([old_snake_x, old_snake_y])
    score += 1
    # get new random coords for prey
    prey_x, prey_y = place_new_prey(snake)

  print('snake', snake)
  draw_board(snake)
  sleep(0.3)