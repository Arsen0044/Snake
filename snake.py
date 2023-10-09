from tkinter import *
import random

# Створення змійки
class Snake:

    def __init__(self):
        self.squares_list = []
        self.coords_list = []

        for coord in range(snake_lenght):
            square = [0,0,0+SIZE_OF_NET,0+SIZE_OF_NET]
            self.coords_list.append(square)
        for i in self.coords_list:
            square = canvas.create_rectangle(0,0,0+SIZE_OF_NET,0+SIZE_OF_NET,fill='#00FF00')
            self.squares_list.append(square)

# Створення їжі
class Food:

    def __init__(self):
        global FOOD
        x = (random.randint(0, int(WIDTH/SIZE_OF_NET)-1))*SIZE_OF_NET
        y = (random.randint(0, int(HEIGHT/SIZE_OF_NET) - 1))*SIZE_OF_NET
        FOOD = canvas.create_oval(x,y,x+SIZE_OF_NET,y+SIZE_OF_NET,fill='red')

# Основна функція яка рухає змійку та змінює її напрямок руху
def next_turn(snake):

    global direction, snake_lenght, FOOD

    # Перевірка чи гравець з'їв їжу і виконання відповідних дій
    go = 0
    food_coords = canvas.coords(FOOD)
    head_coords = snake.coords_list[0]
    if food_coords[0] == head_coords[0]:
        if food_coords[1] == head_coords[1]:
            canvas.delete(FOOD)
            x = (random.randint(0, int(WIDTH / SIZE_OF_NET) - 1)) * SIZE_OF_NET
            y = (random.randint(0, int(HEIGHT / SIZE_OF_NET) - 1)) * SIZE_OF_NET
            for square in snake.coords_list:
                if square[0] == x and square[1] == y:
                    x = (random.randint(0, int(WIDTH / SIZE_OF_NET) - 1)) * SIZE_OF_NET
                    y = (random.randint(0, int(HEIGHT / SIZE_OF_NET) - 1)) * SIZE_OF_NET
            FOOD = canvas.create_oval(x, y, x + SIZE_OF_NET, y + SIZE_OF_NET, fill='red')
            go = 1
    # Рух змійки за заданим напрямком
    x = snake.coords_list[0][0]
    y = snake.coords_list[0][1]
    if direction == "down":
        y += SIZE_OF_NET
    if direction == "up":
        y -= SIZE_OF_NET
    if direction == "left":
        x -= SIZE_OF_NET
    if direction == "right":
        x += SIZE_OF_NET

    snake.coords_list.insert(0,(x,y))

    square = canvas.create_rectangle(x,y,x+SIZE_OF_NET,y+SIZE_OF_NET,fill="#00FF00")

    snake.squares_list.insert(0,square)

    # Подовження змійки на 1 вразі коли граєць з'їв їжу
    if go == 0:
        canvas.delete(snake.squares_list[-1])
        canvas.delete(snake.coords_list[-1])

        del snake.squares_list[-1]
        del snake.coords_list[-1]

    # Перевірка на програш та встановлення швидкості змійки
    if game_over():
        return False
    else:
        window.after(SPEED,next_turn, snake)

# Функція яка змінює напрямок руху змійки у напрямку відповідно нажатої кнопки
def change_direction(num):

    global direction

    if num == 1 and direction != "down":
        direction = "up"
    elif num == 2 and direction != "up":
        direction = "down"
    elif num == 3 and direction != "right":
        direction = "left"
    elif num == 4 and direction != "left":
        direction = "right"

# Функція яка закінчує гру в разі програшу
def game_over():

    global snake

    if snake.coords_list[0][0] == WIDTH or snake.coords_list[0][0] < 0:
        canvas.delete(ALL)
        x = float(WIDTH/2)
        y = float(HEIGHT/2)
        canvas.create_text(x,y,text="GAME OVER",font=("Consolas",40),fill='red')
        return True
    if snake.coords_list[0][1] == HEIGHT or snake.coords_list[0][1] < 0:
        canvas.delete(ALL)
        x = float(WIDTH/2)
        y = float(HEIGHT/2)
        canvas.create_text(x,y,text="GAME OVER",font=("Consolas",40),fill='red')
        return True
    new_coords_list = snake.coords_list[1:]
    for head in new_coords_list:
        if snake.coords_list[0][0] == head[0]:
            if snake.coords_list[0][1] == head[1]:
                canvas.delete(ALL)
                x = float(WIDTH / 2)
                y = float(HEIGHT / 2)
                canvas.create_text(x, y, text="GAME OVER", font=("Consolas", 40), fill='red')
                return True
    return False

HEIGHT = 700
WIDTH = 1000
SIZE_OF_NET = 50
FOOD = None
SPEED = 80
direction = "down"
snake_lenght = 3

window = Tk()
window.title("Snake Game!")
window.resizable(False,False)

# Розміщення вікна по центру екрану
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - WIDTH) // 2
y = (screen_height - HEIGHT) // 2

window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y-50}")

canvas = Canvas(window,height=HEIGHT,width=WIDTH,bg="#000000")
canvas.pack()

food = Food()
snake = Snake()

window.bind("<Left>", lambda event,num=3:change_direction(num))
window.bind("<Right>",lambda event,num=4:change_direction(num))
window.bind("<Up>",lambda event,num=1:change_direction(num))
window.bind("<Down>",lambda event,num=2:change_direction(num))

next_turn(snake)

window.mainloop()