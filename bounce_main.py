# スペースを押せばゲームが始まるプログラムを追加した
# Gameover画面とpress space画面を表示するプログラムを追加した
#block

from tkinter import *
import random


class Ball:
    def __init__(self, canvas, paddle, block, color):
        self.canvas = canvas
        self.paddle = paddle
        self.block = block
        self.id = canvas.create_oval(0, 284, 15, 299, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.canvas.bind_all('<KeyPress-space>', self.start)

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def hit_block(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        block_pos = self.canvas.coords(self.block.id)
        if block_pos:
            if pos[1]<=block_pos[3] and pos[1] > block_pos[1]:
                if pos[0]< block_pos[2]-3 and pos[0] > block_pos[0]+3:
                    if self.y / abs(self.y) == -1:
                        self.y = abs(self.y)
                        self.canvas.delete(self.block.id)

            if pos[3]>=block_pos[1] and pos[3] < block_pos[3]:
                if pos[0]<block_pos[2]-3 and pos[0] > block_pos[0]+3:
                    if self.y / abs(self.y) == 1:
                        self.y = abs(self.y) * -1
                        self.canvas.delete(self.block.id)

            if pos[0] <= block_pos[2] and pos[0] > block_pos[0]:
                if pos[1] < block_pos[3]-2 and pos[1] > block_pos[1]+2:
                    if self.x / abs(self.x) == -1:
                        self.x = abs(self.x)
                        self.canvas.delete(self.block.id)
            if pos[2] >= block_pos[0] and pos[2] < block_pos[2]:
                if pos[1] < block_pos[3]-2 and pos[1] > block_pos[1]+2:
                    if self.x / abs(self.x) == 1:
                        self.x = abs(self.x) * -1
                        self.canvas.delete(self.block.id)
        else:
            pass

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = abs(self.y)

        if pos[3] >= self.canvas_height:
            # self.y = abs(self.y) * -1
            self.hit_bottom = True

        if pos[0] <= 0:
            self.x = abs(self.x)

        if pos[2] >= self.canvas_width:
            self.x = abs(self.x) * -1

        if self.hit_paddle(pos):
            self.y = abs(self.y) * -1

    def start(self, event):
        if self.y == 0:
            self.x = random.choice((-3, -2, -1, 1, 2, 3))
            self.y = -3


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 400)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, event):
        self.x = -5

    def turn_right(self, event):
        self.x = 5


class Block:
    def __init__(self, canvas, color,  margin_left, margin_top):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 50, fill=color)
        self.canvas.move(self.id, margin_left, margin_top)



class Gameover:
    def __init__(self, canvas):
        self.canvas = canvas
        self.label = Label(text="Game Over", font=(100)).pack()

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

game_over_text = canvas.create_text(250, 200, text='GAME OVER!', state='hidden',font=("Purisa",50))
game_start_text = canvas.create_text(250,200, text='Press space!', state='hidden',font=("purisa",50))
margin_left=200
margin_top=80
paddle = Paddle(canvas, 'blue')
#block=[Block(canvas,'black', margin )for margin in range(10,400,110)]
block=Block(canvas,'black',margin_left,margin_top)
ball = Ball(canvas, paddle, block, 'red')


def update():
    if  ball.hit_bottom == False:
        if ball.x == 0:
            canvas.itemconfig(game_start_text, state='normal')
        else:
            canvas.itemconfig(game_start_text, state='hidden')
        ball.draw()
        ball.hit_block()
        paddle.draw()
        tk.update_idletasks()
        tk.update()
        tk.after(10, update)

    else:
        canvas.itemconfig(game_over_text, state='normal')
tk.after(10, update)
tk.mainloop()