import arcade
import numpy as np
from PIL import Image
import fileHelper
from people import SecretAgent, Enemy
import time
import Utils


NUM_ROOMS = 1
if NUM_ROOMS > 1:
    CHOSEN_ROOM = np.random.randint(1, NUM_ROOMS)
else:
    CHOSEN_ROOM = 1
ROOM_ATTRIBUTES = fileHelper.AccessRoomInfo(CHOSEN_ROOM)

SCREEN_WIDTH = ROOM_ATTRIBUTES.roomWidth
SCREEN_HEIGHT = ROOM_ATTRIBUTES.roomHeight
SPRITE_SCALING_BULLET = (1 / 10)
TITLE = "Siege Simulator"
MOVEMENT_SPEED = 4
ENEMY_MOVEMENT_SPEED = 1
BULLET_SPEED = 12


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=False)
        self.set_location(100, 100)

        self.player_sprite = None
        self.background = None
        self.physics_engine = None
        self.wall_list = EnvGenerator().wall_list
        self.bullet_list = arcade.SpriteList()
        self.barrier_list = None
        self.enemy_list = []  # update each enemy individually

        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

        # Gun firing sounds:
        self.gun_sound = arcade.sound.load_sound("Audio/pistol.wav")
        self.hit_sound = arcade.sound.load_sound("Audio/hitmarker.mp3")

        arcade.set_background_color(arcade.color.ANTIQUE_BRASS)

    def on_draw(self):
        arcade.start_render()
        # draw background, walls, agent, and enemies
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.wall_list.draw()
        self.player_sprite.draw()
        self.bullet_list.draw()

        for enemy in self.enemy_list:
            enemy.player_sprite.draw()

            current_time = time.time()
            if enemy.sees_agent and current_time - enemy.timer >= 0.5:
                self.fire_bullet(enemy)
                enemy.timer = current_time

        if self.enemy_list[0].path:
            arcade.draw_line_strip(self.enemy_list[0].path, arcade.color.BLUE, 2)

    def setup(self, playerHealth: int = 3):
        # create the secret agent
        self.player_sprite = SecretAgent(playerHealth,
                                         ROOM_ATTRIBUTES.agentStart[0],
                                         ROOM_ATTRIBUTES.agentStart[0],
                                         SCREEN_WIDTH,
                                         SCREEN_HEIGHT,
                                         ROOM_ATTRIBUTES.agentScale).player_sprite

        self.background = arcade.load_texture("Images/RoomOption" + str(CHOSEN_ROOM) + "/room.jpeg")
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        for enemy_start in ROOM_ATTRIBUTES.enemyStart:
            new_enemy = Enemy(enemy_start[0],
                              enemy_start[1],
                              SCREEN_WIDTH,
                              SCREEN_HEIGHT,
                              ROOM_ATTRIBUTES.agentScale)

            # also create the barrier list for the A* algorithm
            left_boundary = 20
            right_boundary = SCREEN_WIDTH - 20
            bottom_boundary = 20
            top_boundary = SCREEN_HEIGHT - 20
            enemy_size = new_enemy.player_sprite.width / 2
            new_enemy.barrier_list = arcade.AStarBarrierList(new_enemy.player_sprite, self.wall_list, enemy_size,
                                                             left_boundary, right_boundary, bottom_boundary,
                                                             top_boundary)
            self.enemy_list.append(new_enemy)

    # Movement Functions:
    def fire_bullet(self, person):
        bullet = arcade.Sprite("Images/bullet.png", SPRITE_SCALING_BULLET)
        if type(person) == Enemy:
            e_pos = (person.player_sprite.center_x, person.player_sprite.center_y)
            a_pos = (self.player_sprite.center_x, self.player_sprite.center_y)
            angle = Utils.angle(a_pos, e_pos) - 90
        else:
            angle = person.player_sprite.angle

        bullet.change_x = np.cos(angle * (np.pi / 180)) * BULLET_SPEED
        bullet.change_y = np.sin(angle * (np.pi / 180)) * BULLET_SPEED

        shape_w = person.player_sprite.shape[0]
        shape_h = person.player_sprite.shape[1]
        canter_x, center_y = person.player_sprite.center_x, person.player_sprite.center_y
        bullet.center_x = np.cos(angle * (np.pi / 180)) * (shape_w / 2) + canter_x
        bullet.center_y = np.sin(angle * (np.pi / 180)) * (shape_h / 2) + center_y

        bullet.angle = angle
        self.bullet_list.append(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.moveLeft = True
        elif key == arcade.key.W:
            self.moveUp = True
        elif key == arcade.key.S:
            self.moveDown = True
        elif key == arcade.key.D:
            self.moveRight = True
        elif key == arcade.key.L:
            self.player_sprite.change_angle = -3.0
        elif key == arcade.key.K:
            self.player_sprite.change_angle = 3.0
        elif key == arcade.key.SPACE:
            self.fire_bullet(self)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.moveLeft = False
        elif key == arcade.key.W:
            self.moveUp = False
        elif key == arcade.key.S:
            self.moveDown = False
        elif key == arcade.key.D:
            self.moveRight = False
        elif key == arcade.key.L:
            self.player_sprite.change_angle = 0.0
        elif key == arcade.key.K:
            self.player_sprite.change_angle = 0.0

    def on_update(self, deltaTime):
        self.player_sprite.angle += self.player_sprite.change_angle
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        agentShape = self.player_sprite.shape
        agentXCoord = self.player_sprite.center_x
        agentYCoord = self.player_sprite.center_y

        if self.moveUp and not self.moveDown and ((agentYCoord + agentShape[1] / 2) < SCREEN_HEIGHT):
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.moveDown and not self.moveUp and ((agentYCoord - agentShape[1] / 2 - 10) > 0):
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif self.moveLeft and not self.moveRight and ((agentXCoord - agentShape[0] / 2) > 0):
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.moveRight and not self.moveLeft and ((agentXCoord + agentShape[0] / 2) < SCREEN_WIDTH):
            self.player_sprite.change_x = MOVEMENT_SPEED

        # now update the bullet
        self.bullet_list.update()
        for bullet in self.bullet_list:
            collisions = arcade.check_for_collision_with_list(bullet, self.wall_list)
            if len(collisions) > 0:
                bullet.remove_from_sprite_lists()

            offScreen = (bullet.bottom > SCREEN_WIDTH) or (bullet.top < 0) or (bullet.right < 0) or (
                    bullet.left > SCREEN_WIDTH)
            if offScreen:
                bullet.remove_from_sprite_lists()

        self.player_sprite.update()

        # the A* heuristics path finding for the enemy
        for enemy in self.enemy_list:
            if enemy.path is None:
                self.update_path(enemy)

            # now have the enemy move to the destination
            self.change_enemy_pos(enemy)

            x_dest_complete = (enemy.path[0][0] - 2 < enemy.player_sprite.center_x < enemy.path[0][0] + 2)
            y_dest_complete = (enemy.path[0][1] - 2 < enemy.player_sprite.center_y < enemy.path[0][1] + 2)
            if x_dest_complete and y_dest_complete:
                enemy.path = enemy.path[1:]
                if len(enemy.path) == 0:
                    self.update_path(enemy)

            # now change the enemy angle
            self.change_enemy_angle(enemy)

            # finally, check to see if the enemy sees and should fire at the agent
            # self.shoot_at_agent(enemy)
            self.enemy_sees_agent(enemy)

            enemy.player_sprite.update()

        self.physics_engine.update()

    def change_enemy_angle(self, enemy: Enemy):
        if enemy.current_destination is None or enemy.current_destination != enemy.path[0]:
            enemy.current_destination = enemy.path[0]

            enemy_angle = int(enemy.player_sprite.angle)
            enemy_dest = enemy.path[0]
            pos = enemy.player_sprite.center_x, enemy.player_sprite.center_y
            needed_angle = Utils.angle(pos, enemy_dest)
            if needed_angle - 5 < enemy_angle < needed_angle + 5:
                enemy.player_sprite.angle = enemy_angle
            enemy.player_sprite.angle = needed_angle

    def change_enemy_pos(self, enemy: Enemy):
        change_x, change_y = 0, 0
        if len(enemy.path) == 0:
            enemy.found_goal = True
            pass
        else:
            go_to_coords = enemy.path[0]
            if enemy.player_sprite.center_x < go_to_coords[0]:
                if enemy.player_sprite.center_x + ENEMY_MOVEMENT_SPEED > go_to_coords[0]:
                    change_x = go_to_coords[0] - enemy.player_sprite.center_x
                else:
                    change_x = ENEMY_MOVEMENT_SPEED
            elif enemy.player_sprite.center_x > go_to_coords[0]:
                if enemy.player_sprite.center_x - ENEMY_MOVEMENT_SPEED < go_to_coords[0]:
                    change_x = enemy.player_sprite.center_x - go_to_coords[0]
                else:
                    change_x = -ENEMY_MOVEMENT_SPEED
            if enemy.player_sprite.center_y < go_to_coords[1]:
                if enemy.player_sprite.center_y + ENEMY_MOVEMENT_SPEED > go_to_coords[1]:
                    change_y = go_to_coords[1] - enemy.player_sprite.center_y
                else:
                    change_y = ENEMY_MOVEMENT_SPEED
            elif enemy.player_sprite.center_y > go_to_coords[1]:
                if enemy.player_sprite.center_y - ENEMY_MOVEMENT_SPEED < go_to_coords[1]:
                    change_y = enemy.player_sprite.center_x - go_to_coords[0]
                else:
                    change_y = -ENEMY_MOVEMENT_SPEED

        # update the changed position
        enemy.player_sprite.change_x, enemy.player_sprite.change_y = change_x, change_y

    def update_path(self, enemy: Enemy):
        while enemy.path is None or len(enemy.path) == 0:
            # find if the new destination hits a wall
            valid = False
            new_dest_x = np.random.randint(20, SCREEN_WIDTH - 20)
            new_dest_y = np.random.randint(20, SCREEN_HEIGHT - 20)
            enemy_pos = enemy.player_sprite.position
            while not valid:
                new_dest_x = np.random.randint(20, SCREEN_WIDTH - 20)
                new_dest_y = np.random.randint(20, SCREEN_HEIGHT - 20)
                valid = self.valid_new_dest(enemy_pos, new_dest_x, new_dest_y)

            # calculate the A* path for it
            enemy.path = arcade.astar_calculate_path(enemy_pos, (new_dest_x, new_dest_y),
                                                     enemy.barrier_list, diagonal_movement=True)
        enemy.following_agent = False
        enemy.current_destination = enemy.path[0]

    def valid_new_dest(self, enemy_pos: int(), x: int, y: int) -> bool:
        wall_width = self.wall_list[0].width + 5
        dist = ((enemy_pos[0] - x) ** 2 + (enemy_pos[1] - y) ** 2) ** 0.5
        if dist < 40:
            return False
        for wall in ROOM_ATTRIBUTES.wallCoords:
            within_x = (wall["start"][0] - wall_width) < x < (wall["end"][0] + wall_width)
            within_y = (wall["start"][1] - wall_width) < y < (wall["end"][1] + wall_width)
            if within_x and within_y:
                return False
        return True

    def enemy_sees_agent(self, enemy: Enemy):
        fov = enemy.field_of_view
        agent_center_x = self.player_sprite.center_x
        agent_center_y = self.player_sprite.center_y
        enemy_center_x = enemy.player_sprite.center_x
        enemy_center_y = enemy.player_sprite.center_y
        enemy_angle = enemy.player_sprite.angle + 90

        dist = ((agent_center_x-enemy_center_x)**2 + (agent_center_y-enemy_center_y)**2)**0.5
        r = max((dist * fov)/2, 50)  # set a minimum FOV of 50
        line_of_sight_coords = (np.cos(enemy_angle * (np.pi / 180)) * dist + enemy_center_x,
                                np.sin(enemy_angle * (np.pi / 180)) * dist + enemy_center_y)

        d = ((line_of_sight_coords[0]-agent_center_x)**2 + (line_of_sight_coords[1]-agent_center_y)**2)**0.5

        # if the enemy sees, the agent, fire a bullet and create new A* path
        if r**2 > d**2:
            enemy_pos = enemy.player_sprite.position

            enemy.sees_agent = True
            current_time = time.time()
            print(current_time - enemy.timer)

            if not enemy.following_agent:
                enemy.path = arcade.astar_calculate_path(enemy_pos, (agent_center_x, agent_center_y),
                                                     enemy.barrier_list, diagonal_movement=True)
                enemy.following_agent = True
                enemy.timer = time.time()
            print("sees agent")

        else:
            enemy.sees_agent = False


class EnvGenerator(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.generate_room()

    def generate_room(self):
        im = Image.open("Images/wall.png")
        initWallSize = im.size
        wallSize = int((SCREEN_WIDTH * SCREEN_HEIGHT) * (1 / 70))
        wallScale = initWallSize[0] / wallSize
        newWallSize = int(wallScale * initWallSize[0])

        wallList = ROOM_ATTRIBUTES.wallCoords
        for listItem in wallList:
            start = listItem["start"]
            end = listItem["end"]

            if start[0] != end[0]:
                for x in range(start[0], end[0], newWallSize):
                    wall = arcade.Sprite("Images/wall.png", wallScale)
                    wall.center_x = x
                    wall.center_y = SCREEN_HEIGHT - start[1]
                    self.wall_list.append(wall)

            else:
                for y in range(start[1], end[1], newWallSize):
                    wall = arcade.Sprite("Images/wall.png", wallScale)
                    wall.center_x = start[0]
                    wall.center_y = SCREEN_HEIGHT - y
                    self.wall_list.append(wall)


def __main__():
    game = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    __main__()
