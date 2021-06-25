import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


from functools import partial

class EVTrainingScreen(GridLayout):
    def __init__(self, **kwargs):
        super(EVTrainingScreen, self).__init__(**kwargs)
        self.counter = 0
        self.cols = 5
        self.count_lbl = Label(text = str(self.counter))
        self.add_widget(self.count_lbl)
        self.btn1 = Button(text = "+1 EV")
        self.btn2 = Button(text = "+2 EV")
        self.btn3 = Button(text = "+3 EV")
        self.btn4 = Button(text = "-1 EV")
        self.btn1.bind(on_press = partial(self.updateCounter, 1))
        self.btn2.bind(on_press = partial(self.updateCounter, 2))
        self.btn3.bind(on_press = partial(self.updateCounter, 3))
        self.btn4.bind(on_press = partial(self.updateCounter, -1))
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)
        self.add_widget(self.btn4)
        
        
    def addCounter(self, value):
        self.counter = self.counter + value
        
    def updateCounter(self, value, *args):
        self.addCounter(value)
        self.count_lbl.text = str(self.counter)
        
        

class MyApp(App):

    def build(self):
    
        return EVTrainingScreen()

if __name__ == '__main__':
    MyApp().run()
