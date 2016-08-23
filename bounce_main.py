from tkinter import *
import random

class Ball:
    def __init__(self, canvas, paddle, block, ball_size, width_number, height_number, color):
        self.canvas = canvas
        self.paddle = paddle
        self.block = block
        #self.clear = clear
        self.id = canvas.create_oval(0, 0, ball_size, ball_size, fill=color)
        self.canvas.move(self.id, 245, 384)
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.canvas.bind_all('<KeyPress-space>', self.start)
        self.width_number = width_number
        self.height_number = height_number


    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def hit_block(self):
        #self.count = self.width_number * height_number
        pos = self.canvas.coords(self.id)
        for h in range(height_number):
            for i in range(width_number*h,width_number*h+width_number):
                block_pos = [i for i in range(width_number*height_number)]
                block_pos[i] = self.canvas.coords(self.block.id[i])
                if block_pos[i]:
                    if pos[1]<=block_pos[i][3] and pos[1] > block_pos[i][1]:
                        if pos[0]< block_pos[i][2]-3 and pos[0] > block_pos[i][0]+3:
                            if self.y / abs(self.y) == -1:
                                self.y = abs(self.y) + 0.55
                                self.canvas.delete(self.block.id[i])
         #                       self.count -= 1

                    if pos[3]>=block_pos[i][1] and pos[3] < block_pos[i][3]:
                        if pos[0]<block_pos[i][2]-3 and pos[0] > block_pos[i][0]+3:
                            if self.y / abs(self.y) == 1:
                                self.y = abs(self.y) * -1 -0.55
                                self.canvas.delete(self.block.id[i])
          #                      self.count -= 1

                    if pos[0] <= block_pos[i][2] and pos[0] > block_pos[i][0]:
                        if pos[1] < block_pos[i][3]-2 and pos[1] > block_pos[i][1]+2:
                            if self.x / abs(self.x) == -1:
                                self.x = abs(self.x) + 0.55
                                self.canvas.delete(self.block.id[i])
           #                     self.count -= 1

                    if pos[2] >= block_pos[i][0] and pos[2] < block_pos[i][2]:
                        if pos[1] < block_pos[i][3]-2 and pos[1] > block_pos[i][1]+2:
                            if self.x / abs(self.x) == 1:
                                self.x = abs(self.x) * -1 - 0.55
                                self.canvas.delete(self.block.id[i])
            #                    self.count -= 1

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
            self.y = -2

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
        self.x = -4

    def turn_right(self, event):
        self.x = 4


class Block:
    def __init__(self, canvas, width_number, height_number, margin_left, block_width, block_height, margin_top, color):
        self.canvas = canvas
        self.id = [canvas.create_rectangle(0, 0, block_width, block_height, fill=color)for i in range(width_number*height_number)]
        for h in range(height_number):
            for w in range(width_number*h,width_number+width_number*h):
                self.canvas.move(self.id[w],
                    (margin_left+block_width*w+margin_left*w)-(block_width*width_number+margin_left*width_number)*h,
                    margin_top+block_height*h+margin_top*h)

"""""
class Clear:
    def __init__(self,canvas):
        self.canvas = canvas

    def count(self):
        self.canvas.itemconfig(self.canvas.create_text(450, 300,
            text='{0}'.format(self.block.count), state='hidden', font=("Purisa", 50)), state='normal')
"""""


# config(screen)
screen_width = 500
screen_height = 500

# config(block)
width_number = 4
height_number = 3
block_width = 110
block_height = 30
margin_left = 10
margin_top = 10
block_color = 'gray'

# config(ball)
ball_color = 'red'
ball_size = 15

# config(paddle)
paddle_color = 'blue'

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
c = Canvas(tk, width=screen_width, height=screen_height, bd=0, highlightthickness=0)
c.pack()
tk.update()

game_over_text = c.create_text(250, 200, text='GAME OVER!', state='hidden', font=("Purisa", 50))
game_start_text = c.create_text(250, 200, text='Press space!', state='hidden', font=("purisa", 50))

#clear = Clear(c)
p = Paddle(c, paddle_color)
b = Block(c, width_number, height_number, margin_left, block_width, block_height, margin_top, block_color)
ball = Ball(c, p, b, ball_size, width_number, height_number, ball_color)


def update():
    if  ball.hit_bottom == False:
        if ball.x == 0:
            c.itemconfig(game_start_text, state='normal')
        else:
            c.itemconfig(game_start_text, state='hidden')
        ball.draw()
        ball.hit_block()
        p.draw()
#        clear.count()
        tk.update_idletasks()
        tk.update()
        tk.after(10, update)

    else:
        c.itemconfig(game_over_text, state='normal')
tk.after(10, update)
tk.mainloop()