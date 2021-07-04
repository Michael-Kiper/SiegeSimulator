import time
import arcade
from PIL import Image


class SecretAgent(arcade.Sprite):
    def __init__(self, health: int, start_x: int, start_y: int, screen_width: int, screen_height: int, scale: int):
        super().__init__()
        self.player_sprite = arcade.Sprite("Images/agent.gif")
        self.player_sprite.center_x = start_x
        self.player_sprite.center_y = start_y
        self.player_sprite.health = health
        self.player_sprite.hit_box_algorithm = "Simple"

        im = Image.open("Images/agent.gif")

        desiredScale = (screen_width * screen_height) * scale / (im.size[0] * im.size[1])
        self.player_sprite.scale = float(desiredScale)
        self.player_sprite.shape = (int(im.size[0] * desiredScale), int(im.size[1] * desiredScale))


class Enemy(arcade.Sprite):
    def __init__(self, start_x: int, start_y: int, screen_width: int, screen_height: int, scale: int):
        super().__init__()
        self.player_sprite = arcade.Sprite("Images/police.png")
        self.player_sprite.center_x = start_x
        self.player_sprite.center_y = start_y
        self.player_sprite.health = 2
        self.player_sprite.hit_box_algorithm = "Simple"
        self.barrier_list = None

        im = Image.open("Images/police.png")

        desiredScale = (screen_width * screen_height) * scale / (im.size[0] * im.size[1])
        self.player_sprite.scale = float(desiredScale) * 1.8
        self.player_sprite.shape = (int(im.size[0] * desiredScale), int(im.size[1] * desiredScale))

        self.path = None
        self.current_destination = None

        self.field_of_view = 0.5
        self.sees_agent = False
        self.timer = time.time()
