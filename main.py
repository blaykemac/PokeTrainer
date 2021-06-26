import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen

from functools import partial



class EVTrainingLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(EVTrainingLayout, self).__init__(**kwargs)
        self.counter = 0
        self.pokerus = False
        self.noitem = True
        self.macho = False
        self.power = False
        self.orientation = "vertical"
        self.spacing = 10
        self.buttons = []
        
        
        
        self.row1 = BoxLayout(spacing=10)
        self.row2 = BoxLayout(spacing=10)
        self.row3 = BoxLayout(spacing=10)
        self.add_widget(self.row1)
        self.add_widget(self.row2)
        self.add_widget(self.row3)
        
        self.pokemonLogo = Image(source="pokeball.png")
        
        self.count_lbl = Label(text = "EVs : 0")
        self.count_lbl.color = (0,0,0,1)
        self.row1.add_widget(self.pokemonLogo)
        self.row1.add_widget(self.count_lbl)
        
        self.btn_noitem = Button(text = "No Held Item")
        self.btn_macho = Button(text = "Macho Brace")
        self.btn_power = Button(text = "Power Item")
        self.btn_pokerus = Button(text = "No Pokerus")
        self.buttons.append(self.btn_noitem)
        self.buttons.append(self.btn_macho)
        self.buttons.append(self.btn_power)
        self.buttons.append(self.btn_pokerus)

        self.btn_noitem.bind(on_press = partial(self.switchItem, 1))
        self.btn_macho.bind(on_press = partial(self.switchItem, 2))
        self.btn_power.bind(on_press = partial(self.switchItem, 3))
        self.btn_pokerus.bind(on_press = partial(self.togglePokerus))
        self.row2.add_widget(self.btn_noitem)
        self.row2.add_widget(self.btn_macho)
        self.row2.add_widget(self.btn_power)
        self.row2.add_widget(self.btn_pokerus)
        
        
        self.btn1 = Button(text = "+1 EV")
        self.btn2 = Button(text = "+2 EV")
        self.btn3 = Button(text = "+3 EV")
        self.btn4 = Button(text = "-1 EV")
        self.btn5 = Button(text = "Clear EVs")
        self.buttons.append(self.btn1)
        self.buttons.append(self.btn2)
        self.buttons.append(self.btn3)
        self.buttons.append(self.btn4)
        self.buttons.append(self.btn5)

        self.btn1.bind(on_press = partial(self.updateCounter, 1))
        self.btn2.bind(on_press = partial(self.updateCounter, 2))
        self.btn3.bind(on_press = partial(self.updateCounter, 3))
        self.btn4.bind(on_press = partial(self.updateCounter, -1))
        self.btn5.bind(on_press = partial(self.updateCounter, 0))
        
        self.row3.add_widget(self.btn1)
        self.row3.add_widget(self.btn2)
        self.row3.add_widget(self.btn3)
        self.row3.add_widget(self.btn4)
        self.row3.add_widget(self.btn5)

        
        for button in self.buttons:
            button.background_normal = ""
            button.background_color = (0.5,0.5,0.5,1)
            
        self.btn_noitem.background_color = (0.67,0.5,1,1)
        
        
    def togglePokerus(self, *args):
        self.pokerus = not self.pokerus
        #Now update toggle button state
        if self.pokerus:
            self.btn_pokerus.background_color = (1,0.2,0.6,1)#(255/255.0, 51/255.0, 153/255.0, 1)
            self.btn_pokerus.text = "Pokerus"
        else:
            self.btn_pokerus.background_color = (0.5,0.5,0.5,1)
            self.btn_pokerus.text = "No Pokerus"

    def switchItem(self, item_id, *args):
        self.noitem = False
        self.macho = False
        self.power = False        
        
        self.btn_noitem.background_color = (0.5,0.5,0.5,1)
        self.btn_macho.background_color = (0.5,0.5,0.5,1)
        self.btn_power.background_color = (0.5,0.5,0.5,1)
        
        if item_id == 1:
            self.noitem = True
            self.btn_noitem.background_color = (0.67,0.5,1,1)
            
            
        if item_id == 2:
            self.macho = True
            self.btn_macho.background_color = (0.67,0.5,1,1)
            
        if item_id == 3:
            self.power = True
            self.btn_power.background_color = (0.67,0.5,1,1)
            
        
        
    def addCounter(self, value):
        self.counter = self.counter + value
        
    def resetCounter(self):
        self.counter = 0
        
    def updateCounter(self, value, *args):
        if self.macho:
            modified_value = value * 2
        elif self.power:
            modified_value = value + 8
        else:
            modified_value = value
        
        if self.pokerus:
            modified_value = modified_value * 2
        
        if value == 0:
            self.resetCounter()
        elif value <= 0:
            self.addCounter(value)
        else:
            self.addCounter(modified_value)
        
        self.count_lbl.text = "EVs : " + str(self.counter)
        


Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        Label:
            text : "Welcome to the PokeTrainer app."
        Button:
            text: "Go to EV training"
            on_press: root.manager.current = "ev"
        
<EVScreen>:
    BoxLayout:
        Button:
            text: "Go to home screen"
            on_press: root.manager.current = "home"

""")

#Declare screens
class HomeScreen(Screen):
    pass
    
class EVScreen(Screen):
    pass

class MyApp(App):

    def build(self):
    
        # Define the window name
        self.title = "PokeTrainer"
        self.icon = "pokeball.png"
        
        #Create screen manager
        self.sm = ScreenManager()
        
        #Add different screens
        self.hs = HomeScreen(name="home")
        self.sm.add_widget(self.hs)
        self.es = EVScreen(name="ev")
        self.ev_layout = EVTrainingLayout()
        self.ev_layout.bind(pos = self._update_rect, size = self._update_rect)
        self.es.add_widget(self.ev_layout)
        self.sm.add_widget(self.es)
        
        
        
        with self.ev_layout.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(size = self.ev_layout.size, pos = self.ev_layout.pos)
            
        self.sound = SoundLoader.load("pokemon_theme.wav")
        if self.sound:
            self.sound.loop = True
            self.sound.volume = 0.1
            self.sound.play()
        
        return self.sm
       
    def _update_rect(self,instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    MyApp().run()
