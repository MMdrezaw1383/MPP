from tkinter import *
from random import randint
import os
import sys


class Snake:
    # BODY_SIZE = 2
    def __init__(self):
        self.body_size = BODY_SIZE
        self.squares = []
        self.coordinates = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + GAME_SPACE, y + GAME_SPACE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = randint(0, (GAME_WIDTH // GAME_SPACE) - 1) * GAME_SPACE
        y = randint(0, (GAME_HEIGHT // GAME_SPACE) - 1) * GAME_SPACE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + GAME_SPACE, y + GAME_SPACE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= GAME_SPACE
    elif direction == "down":
        y += GAME_SPACE
    elif direction == "left":
        x -= GAME_SPACE
    elif direction == "right":
        x += GAME_SPACE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + GAME_SPACE, y + GAME_SPACE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score:{score}", font=("Courier", 40))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_game_over(snake):
        game_over()
    else:
        window.after(SLOWNESS, next_turn, snake, food)


def check_game_over(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x+GAME_SPACE > GAME_WIDTH:
        print(x)
        return True

    if y < 0 or y+GAME_SPACE > GAME_HEIGHT:
        return True

    for sq in snake.coordinates[1:]:
        if x == sq[0] and y == sq[1]:
            return True
    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=("Terminal", 80), text="Game Over", fill="#DF1A2F", tag="gameover")


def change_direction(new_dir):
    global direction
    if new_dir == "left":
        if direction != "right":
            direction = new_dir
    elif new_dir == "right":
        if direction != "left":
            direction = new_dir
    elif new_dir == "up":
        if direction != "down":
            direction = new_dir
    elif new_dir == "down":
        if direction != "up":
            direction = new_dir


def restart_program():
    path = sys.executable
    os.execl(path, path, *sys.argv)


GAME_WIDTH = 500
GAME_HEIGHT = 500
GAME_SPACE = 20
SLOWNESS = 100
BODY_SIZE = 2
SNAKE_COLOR = "yellow"
FOOD_COLOR = "red"
BACKGROUND = "black"
score = 0
direction = "down"
# -----------------------------
# use tkinter
window = Tk()
window.title("Snake game")
window.resizable(False, False)
label = Label(window, text=f"Score:{score}", font=("Courier", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

restart = Button(window, text="Restart", fg="red", command=restart_program)
restart.pack()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2)+250)
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{600}x{600}+{x//2}+{y//2}")
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
