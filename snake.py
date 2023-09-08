from tkinter import *
from tkinter.ttk import *
import random
import winsound

BG_COLOR = '#000000'
GAME_HEIGHT = 600
GAME_WIDTH = 600
SPACE = 40
FOOD_COLOR = '#FFFF00'
SNAKE_COLOR = '#FF0000'
B_PART = 3
direction = "down"
SPEED = 150


class Snake:
    def __init__(self):
        self.body_size = B_PART
        self.coordinates = []
        self.squares = []

        for x in range(0, B_PART):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x1 = random.randint(0, (GAME_WIDTH/SPACE)-1) * SPACE
        y1 = random.randint(0, (GAME_HEIGHT/SPACE)-1) * SPACE

        self.coordinates = [x1, y1]
        canvas.create_oval(x1, y1, x1 + SPACE, y1 + SPACE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE
    elif direction == "down":
        y += SPACE
    elif direction == "right":
        x += SPACE
    elif direction == "left":
        x -= SPACE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        winsound.PlaySound("eat_snake.wav", winsound.SND_ASYNC)
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        score = 0
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for BodyPart in snake.coordinates[1:]:
        if x == BodyPart[0] and y == BodyPart[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    winsound.PlaySound("game_over.wav", winsound.SND_ASYNC)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 80), text="GAME OVER", fill='#FF0000')
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.5,
                       font=('consolas', 30), text="press ENTER to restart ", fill='#0000FF')
    change_direction('down')


def hello():

    global canvas

    canvas.delete(ALL)

    food = Food()
    snake = Snake()
    next_turn(snake, food)


window = Tk()
window.title = "Snake Game"
window.resizable(False, False)

score = 0

label = Label(window, text="SCORE :{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

food = Food()
snake = Snake()
next_turn(snake, food)

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<a>', lambda event: hello())


window.mainloop()
