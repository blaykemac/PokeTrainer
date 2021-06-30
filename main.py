# Import all required modules

import kivy

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image, AsyncImage
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest

from functools import partial


# Define layouts

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

        self.pokemon_logo = Image(source="pokeball.png")

        # self.count_lbl = Label(text = "EVs : 0")
        self.count_lbl = LabelW(text="EVs : 0")
        self.count_lbl.color = (0, 0, 0, 1)
        self.row1.add_widget(self.pokemon_logo)
        self.row1.add_widget(self.count_lbl)

        self.btn_noitem = Button(text="No Held Item")
        self.btn_macho = Button(text="Macho Brace")
        self.btn_power = Button(text="Power Item")
        self.btn_pokerus = Button(text="No Pokerus")
        self.buttons.append(self.btn_noitem)
        self.buttons.append(self.btn_macho)
        self.buttons.append(self.btn_power)
        self.buttons.append(self.btn_pokerus)

        self.btn_noitem.bind(on_press=partial(self.switchItem, 1))
        self.btn_macho.bind(on_press=partial(self.switchItem, 2))
        self.btn_power.bind(on_press=partial(self.switchItem, 3))
        self.btn_pokerus.bind(on_press=partial(self.togglePokerus))
        self.row2.add_widget(self.btn_noitem)
        self.row2.add_widget(self.btn_macho)
        self.row2.add_widget(self.btn_power)
        self.row2.add_widget(self.btn_pokerus)

        self.btn1 = Button(text="+1 EV")
        self.btn2 = Button(text="+2 EV")
        self.btn3 = Button(text="+3 EV")
        self.btn4 = Button(text="-1 EV")
        self.btn5 = Button(text="Clear EVs")
        self.buttons.append(self.btn1)
        self.buttons.append(self.btn2)
        self.buttons.append(self.btn3)
        self.buttons.append(self.btn4)
        self.buttons.append(self.btn5)

        self.btn1.bind(on_press=partial(self.updateCounter, 1))
        self.btn2.bind(on_press=partial(self.updateCounter, 2))
        self.btn3.bind(on_press=partial(self.updateCounter, 3))
        self.btn4.bind(on_press=partial(self.updateCounter, -1))
        self.btn5.bind(on_press=partial(self.updateCounter, 0))

        self.row3.add_widget(self.btn1)
        self.row3.add_widget(self.btn2)
        self.row3.add_widget(self.btn3)
        self.row3.add_widget(self.btn4)
        self.row3.add_widget(self.btn5)

        for button in self.buttons:
            button.background_normal = ""
            button.background_color = (0.5, 0.5, 0.5, 1)

        self.btn_noitem.background_color = (0.67, 0.5, 1, 1)

    def togglePokerus(self, *args):
        self.pokerus = not self.pokerus
        # Now update toggle button state
        if self.pokerus:
            self.btn_pokerus.background_color = (1, 0.2, 0.6, 1)  # (255/255.0, 51/255.0, 153/255.0, 1)
            self.btn_pokerus.text = "Pokerus"
        else:
            self.btn_pokerus.background_color = (0.5, 0.5, 0.5, 1)
            self.btn_pokerus.text = "No Pokerus"

    def switchItem(self, item_id, *args):
        self.noitem = False
        self.macho = False
        self.power = False

        self.btn_noitem.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_macho.background_color = (0.5, 0.5, 0.5, 1)
        self.btn_power.background_color = (0.5, 0.5, 0.5, 1)

        if item_id == 1:
            self.noitem = True
            self.btn_noitem.background_color = (0.67, 0.5, 1, 1)

        if item_id == 2:
            self.macho = True
            self.btn_macho.background_color = (0.67, 0.5, 1, 1)

        if item_id == 3:
            self.power = True
            self.btn_power.background_color = (0.67, 0.5, 1, 1)

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


class LabelW(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

    pass


class BoxW(BoxLayout):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

    pass


# Builder.load_string("""
# <HomeScreen>:
# BoxLayout:
# Label:
# text : "Welcome to the PokeTrainer app."
# Button:
# text: "Go to EV training"
# on_press: root.manager.current = "ev"

# <EVScreen>:
# BoxLayout:
# Button:
# text: "Go to home screen"
# on_press: root.manager.current = "home"

# """)

# Declare screens
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.banner = Label(text="PokeTrainer", font_size="50sp")
        self.banner.color = (0, 0, 0, 1)

        self.pokemon_logo = Image(source="pokeball.png")

        self.ev_btn = Button(text="Go to EV training")
        self.ev_btn.bind(on_press=partial(self.change, "ev"))
        self.ev_btn.size_hint = (1, 0.2)

        self.shiny_btn = Button(text="Go to shiny hunting")
        self.shiny_btn.bind(on_press=partial(self.change, "shiny"))
        self.shiny_btn.size_hint = (1, 0.2)

        self.btns = BoxLayout(spacing=10)
        self.btns.add_widget(self.shiny_btn)
        self.btns.add_widget(self.ev_btn)

        self.box = BoxW(orientation="vertical")
        self.box.spacing = 10
        self.box.add_widget(self.banner)
        self.box.add_widget(self.pokemon_logo)
        self.box.add_widget(self.btns)

        # print("self.box.size {}".format(self.box.size))

        # self.bind(size = self._update_rect, pos = self._update_rect)

        # with self.canvas.before:
        #    Color(1,1,1,1)
        #    self.rect = Rectangle(size = self.size, pos = self.pos)

        self.add_widget(self.box)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.pos

    def change(self, screen_id, *args):
        if screen_id == "shiny":
            self.manager.transition.direction = "right"
        elif screen_id == "ev":
            self.manager.transition.direction = "left"

        self.manager.current = screen_id


class EVScreen(Screen):
    def __init__(self, **kwargs):
        super(EVScreen, self).__init__(**kwargs)

        self.home_btn = Button(text="Go to home")
        self.home_btn.bind(on_press=partial(self.change, "home"))
        self.home_btn.size_hint = (1, 0.1)

        self.ev_layout = EVTrainingLayout()

        self.box = BoxW(orientation="vertical")
        self.box.spacing = 10

        self.box.add_widget(self.ev_layout)
        self.box.add_widget(self.home_btn)

        self.add_widget(self.box)

    def change(self, screen_id, *args):
        self.manager.transition.direction = "right"
        self.manager.current = screen_id


class ShinyScreen(Screen):
    def __init__(self, **kwargs):
        super(ShinyScreen, self).__init__(**kwargs)

        self.home_btn = Button(text="Go to home")
        self.home_btn.bind(on_press=partial(self.change, "home"))
        self.home_btn.size_hint = (1, 0.1)

        # self.ev_layout = EVTrainingLayout()

        self.box = BoxW(orientation="vertical")
        self.box.spacing = 10

        # Create text field
        # Create search button
        # Retrieve shiny sprite from internet

        self.search_box = BoxLayout()
        self.search_box.spacing = 10

        def got_json(req, result):
            # for key, value in req.resp_headers.items():
            #    print('{}: {}'.format(key, value))

            # print(result["sprites"]["front_shiny"])
            shiny_url = result["sprites"]["front_shiny"]
            # shiny_img = UrlRequest(shiny_url, get_image)
            self.shiny_img.source = shiny_url

        def get_image(req, result):
            # self.shiny_img.source =
            pass

        def on_enter(instance):
            # print("Instance is {}".format(instance.text))
            search_pokemon = instance.text
            pokemon = UrlRequest("https://pokeapi.co/api/v2/pokemon/" + search_pokemon.lower(), got_json)
            print(pokemon)

        def on_btn_enter(instance):
            search_pokemon = self.search_field.text
            pokemon = UrlRequest("https://pokeapi.co/api/v2/pokemon/" + search_pokemon.lower(), got_json)

        self.search_field = TextInput(hint_text="Search for Pokemon", multiline=False)
        self.search_field.bind(on_text_validate=on_enter)
        self.search_btn = Button(text="Search")
        self.search_btn.bind(on_press=on_btn_enter)
        self.search_box = BoxLayout(orientation="horizontal")
        self.search_box.add_widget(self.search_field)
        self.search_box.add_widget(self.search_btn)

        self.shiny_img = AsyncImage(source="pokeball.png", allow_stretch=True)

        self.box.add_widget(self.search_box)
        self.box.add_widget(self.shiny_img)
        self.box.add_widget(self.home_btn)

        self.add_widget(self.box)

    def change(self, screen_id, *args):
        self.manager.transition.direction = "left"
        self.manager.current = screen_id


class MyApp(App):

    def build(self):
        # Define the window name
        self.title = "PokeTrainer"
        self.icon = "pokeball.png"

        # Create screen manager
        self.sm = ScreenManager()

        # Add different screens
        self.hs = HomeScreen(name="home")
        self.sm.add_widget(self.hs)
        self.es = EVScreen(name="ev")
        # self.ev_layout = EVTrainingLayout()
        # self.ev_layout.bind(pos = self._update_rect, size = self._update_rect)
        # self.es.add_widget(self.ev_layout)
        self.sm.add_widget(self.es)
        self.ss = ShinyScreen(name="shiny")
        self.sm.add_widget(self.ss)

        # with self.sm.canvas.before:
        #    Color(1,1,1,1)
        #    self.sm.rect = Rectangle(size = self.sm.size, pos = self.sm.pos)

        self.sound = SoundLoader.load("pokemon_theme.wav")
        if self.sound:
            self.sound.loop = True
            self.sound.volume = 0.1
            self.sound.play()

        return self.sm

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    MyApp().run()
