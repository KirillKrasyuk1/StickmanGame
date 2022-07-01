from tkinter import *
import time
class Game:
    def __init__(self, width, height):
        self.tk = Tk()
        self.tk.title('Stickman game')
        # self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=width, height=height)
        self.canvas.pack()
        self.tk.update()
        self.ht, self.wh = height, width
        self.bg = PhotoImage(file='background.gif')
        w = self.bg.width()
        h = self.bg.height()
        self.sprites = []
        self.running = True
        for x in range(0, 5):
            for i in range(0, 2):
                self.canvas.create_image(x * w, i * h, image=self.bg, anchor='nw')
    def mainloop(self):
        while self.running == True:
            for sprite in self.sprites:
                sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


class Sprites:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass
    def coordinates(self):
        return self.coordinates

class SpriteCoords:
     def __init__(self, x1=0, y1=0, x2=0, y2=0):
         self.x1 = x1
         self.y1 = y1
         self.x2 = x2
         self.y2 = y2


class PlatformSprite(Sprites):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprites.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = SpriteCoords(x, y, x + width, y + height)


class StickmanSprite(Sprites):
    def __init__(self, game):
        Sprites.__init__(self, game)
        self.move_left = [PhotoImage(file='персонаж.png'), PhotoImage(file='шаг влево.png'), PhotoImage(file='шаг влево 2.png')]
        self.move_right = [PhotoImage(file='персонаж.png'), PhotoImage(file='шаг в право.png'), PhotoImage(file='шаг вправо 2.png')]
        self.image = game.canvas.create_image(200,470, image=self.move_right[0], anchor='nw')
        self.x = 0
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = SpriteCoords()
        game.canvas.bind_all('<KeyPress - a>', self.turn_left)
        game.canvas.bind_all('<KeyPress - d>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

    def jump(self, evt):
        print(self.coordinates)
        if self.y == 0:
            self.y = -3
            self.jump_count = 0

    def animate(self, evt):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time >= 0.1:
                self.last_time = time.time()
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 1:
                    self.current_image_add = 1
                self.current_image += self.current_image_add
                if self.x < 0:
                    self.game.canvas.itemconfig(self.image, image=self.move_left[self.current_image])
                if self.x > 0:
                    self.game.canvas.itemconfig(self.image, image=self.move_right[self.current_image])
                





def within_x(co_1, co_2):
    if(co_1.x1 > co_2.x1 and co_2.x1 < co_2.x2)\
    or(co_1.x2 > co_2.x1 and co_1.x2 < co_2.x1)\
    or(co_2.x1 > co_1.x1 and co_2.x1 < co_1.x2)\
    or(co_2.x2 > co_1.x1 and co_2.x2 < co_1.x2):
        return True
    else:
        return False

def within_y(co_1, co_2):
    if(co_1.y1 > co_2.y1 and co_2.y1 < co_2.y2)\
    or(co_1.y2 > co_2.y1 and co_1.y2 < co_2.y1)\
    or(co_2.y1 > co_1.y1 and co_2.y1 < co_1.y2)\
    or(co_2.y2 > co_1.y1 and co_2.y2 < co_1.y2):
        return True
    else:
        return False

def collided_left(co_1, co_2):
    if within_y(co_1, co_2):
        if(co_1.x2 >= co_2.x1 and co_1.x2 <= co_2.x2):
            return True
    return False

def collided_right(co_1, co_2):
    if within_y(co_1, co_2):
        if(co_1.x2 >= co_2.x1 and co_1.x2 <= co_2.x2):
            return True
    return False

def collided_top(co_1, co_2):
    if within_x(co_1, co_2):
        if(co_1.y1 >= co_2.y1 and co_1.y1 <= co_2.y2):
            return True
    return False

def collided_bottom(y, co_1, co_2):
    if within_x(co_1, co_2):
        y_calc = y + co_1.y2
        if y_calc >= co_2.y1 and y_calc <= co_2.y2:
            return True
    return False


game = Game(128 * 5, 128 * 5)
platform1 = PlatformSprite(game, PhotoImage(file='platform3.gif'), 0, 480, 320, 10)
player = StickmanSprite(game)
game.mainloop()


