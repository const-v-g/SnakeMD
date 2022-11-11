from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.clock import Clock
from kivy.core.window import Window, Keyboard
from kivy.properties import OptionProperty, NumericProperty, ListProperty,  BooleanProperty, StringProperty
from kivy.vector import Vector
from random import randint
from kivy.utils import platform

Builder.load_string('''
<SnakeScreen>:
    md_bg_color: 'grey'
    canvas:
        Color:
            rgba: 0,1,0,1
        Line:
            points: self.points
            width: self.snakeSize
        Color:
            rgba: 1,.5,0,1
        Ellipse:
            pos: self.food
            size: self.foodSize, self.foodSize
    MDGridLayout:
        cols: 3
        size_hint: 1, 0.3
        MDLabel:
            text: root.food_cnt
            valign: 'bottom'
        MDLabel:
            text: root.debstr
        MDGridLayout:
            cols: 3
            MDLabel:
                text: ''
            MDRoundFlatButton:
                text: "Up"
                # md_bg_color: 'red'
                size_hint: 1,1
                on_press: root.do_action('up')
            MDLabel:
                text: ''
            MDRoundFlatButton:
                text: "Left"
                size_hint: 1,1
                on_press: root.do_action('left')
            MDLabel:
                text: ''
            MDRoundFlatButton:
                text: "Right"
                size_hint: 1,1
                on_press: root.do_action('right')
            MDLabel:
                text: ''
            MDRoundFlatButton:
                text: "Down"
                size_hint: 1,1
                on_press: root.do_action('down')
            MDLabel:
                text: ''
''')

class SnakeScreen(MDFloatLayout):
    points = ListProperty([0,0,0,10,10,10])
    foodSize = NumericProperty(10)
    snakeSize = NumericProperty(5)
    food = ListProperty([95,95])
    food_cnt = StringProperty('Съедено - 0')
    debstr = StringProperty('')
    win_x = NumericProperty(500)
    win_y = NumericProperty(500)
    dx = NumericProperty(10)
    dy = NumericProperty(0)
    cnt = NumericProperty(0)

    def build(self):
        w_size = Window.size
        Window.bind(on_key_down=self.key_action)
        Window.bind(on_resize = self.resize_me)
        self.win_x = w_size[0]
        self.win_y = w_size[1]
        dim = self.win_y/50
        if platform == "android":
            dim *= 1.5
        self.dx = dim
        self.dy = 0
        self.foodSize = dim
        self.snakeSize = dim/2
        self.reset_game()
        self.animate()

    def resize_me(self, *args):
        self.clc.cancel()
        self.build()

    def animate(self):
        self.clc = Clock.schedule_interval(self.update_points, 0.1)

    def reset_game(self):
        pnt = []
        cn_x = self.win_x/self.foodSize
        cn_x = int(cn_x/2)*2
        cn_y = self.win_y/self.foodSize
        cn_y = int(cn_y/2)*2
        f_pnt_x = (cn_x/2)*self.foodSize + self.snakeSize
        f_pnt_y = (cn_y/2)*self.foodSize + self.snakeSize
        pnt.append(int(f_pnt_x))
        pnt.append(int(f_pnt_y))
        pnt.append(pnt[0]+self.dx)
        pnt.append(pnt[1]+self.dy)
        pnt.append(pnt[2]+self.dx)
        pnt.append(pnt[3]+self.dy)
       
        self.points = pnt

        self.reset_food()
        self.cnt = 0
        self.food_cnt = f'Съедено - {self.cnt}'

    def reset_food(self):
        cn_x = self.win_x/self.foodSize
        cn_x = int(cn_x/2)*2
        cn_y = self.win_y/self.foodSize
        cn_y = int(cn_y/2)*2
        self.food[0] = randint(2,int(cn_x - 2))*self.foodSize
        self.food[1] = randint(2,int(cn_y - 2))*self.foodSize

    def update_points(self, dt):
        cnt = len(self.points)
        x = self.points[-2]
        y = self.points[-1]
        if x > self.win_x or x < 0:
            self.reset_game()
            return
        if y > self.win_y or y < 0:
            self.reset_game()
            return
        for i in range(0,cnt-2,2):
            if self.points[i] == x and self.points[i+1] == y:
                self.reset_game()
                return
        
        if Vector(x,y).distance((self.food[0]+self.foodSize/2,self.food[1]+self.foodSize/2)) < self.foodSize/2:
            self.points.append(x+self.dx)
            self.points.append(y+self.dy)
            self.reset_food()
            self.cnt += 1
            self.food_cnt = f'Съедено - {self.cnt}'
        else:
            pnt_tmp = []
            for i in range(0,cnt-2):
                pnt_tmp.append(self.points[i+2])
            pnt_tmp.append(x+self.dx)
            pnt_tmp.append(y+self.dy)
            # self.debstr = f'{self.foodSize}\n{self.food[0]} {self.food[1]} \n{pnt_tmp[-2]} {pnt_tmp[-1]}'
            self.points = pnt_tmp

    def do_action(self, key_pressed):
        x = self.points[-2]
        y = self.points[-1]
        match key_pressed:
            case 'up' if self.dy >= 0:
                self.dx = 0
                self.dy = self.foodSize
            case 'right' if self.dx >= 0:
                self.dx = self.foodSize
                self.dy = 0
            case 'down' if self.dy <= 0:
                self.dx = 0
                self.dy = -self.foodSize
            case 'left' if self.dx <= 0:
                self.dx = -self.foodSize
                self.dy = 0
            case 's':
                pass

    def key_action(self, *args):
        key_pressed = Keyboard.keycode_to_string(self, value = list(args)[1])
        self.do_action(key_pressed)
        



class MyApp(MDApp):
    def build(self):
        myScreen = SnakeScreen()
        myScreen.build()
        return myScreen

if __name__ == '__main__':
    MyApp().run()