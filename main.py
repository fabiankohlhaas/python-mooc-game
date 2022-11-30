# Complete your game here
# To import the necessary modules
import pygame
import math
import random


class Game:  # The main game class
    def __init__(self):
        # To define the necessary class variables and initialize pygame
        pygame.init()
        self.load_images()
        self.width = 1280
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))
        self.game_over_font = pygame.font.SysFont("Arial", 32)
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.event_listener = EventListener()
        self.coin_positions = [(20, 15), (140, 15), (295, 15), (20, 198), (140, 198), (295, 198), (20, 610), (140, 610), (295, 610), (620, 340),
                               (370, 15), (950, 15), (1085, 15), (1210, 15), (950, 198), (1085, 198), (1210, 198), (950, 610), (1085, 610), (1210, 610)]
        pygame.display.set_caption("COINBOT")
        self.new_game()
        self.main_loop()

    # To store the filenames of the images used in the game in a list
    def load_images(self):
        self.images = []
        for name in ["coin", "door", "monster", "robot"]:
            self.images.append(pygame.image.load(name + ".png"))

    # To create necessary variables and reset them for a new game
    def new_game(self):
        self.points = 0
        self.robot = Player(
            self.images[3], "robot", 136, 594, self.event_listener)
        self.coin = Coin(self.images[0], self.event_listener)
        self.go_faster = True
        self.game_over = False
        self.left_counter = 0
        self.circle_counter = 0
        self.right_counter = 0
        self.monsters_left()
        self.monster_circle()
        self.monsters_right()

    # To create the monsters on the left side of the screen
    def monsters_left(self):
        starting_xy = [(0, 90), (300, 280), (0, 470)]
        self.left_monsters = []
        for i in range(3):
            monster = self.new_monster()
            monster.rect.x = starting_xy[i][0]
            monster.rect.y = starting_xy[i][1]
            if i != 0 and i & 2 == 0:
                monster.velocity = -monster.velocity
            self.left_monsters.append(monster)

    # To move the monsters on the left side of the screen
    def move_left_monsters(self):
        for i in range(3):
            monster = self.left_monsters[i]
            monster.rect.x += monster.velocity
            if monster.rect.x <= 0:
                monster.velocity = -monster.velocity
            if monster.rect.x >= 300:
                monster.velocity = -monster.velocity

    # To create the monsters in the middle of the screen
    def monster_circle(self):
        self.circle_velocity = 0.01
        self.radius = 240
        self.circle_monsters = []
        for i in range(7):
            monster = self.new_monster()
            monster.velocity = 0
            self.circle_monsters.append(monster)

    # To move the monsters in the middle of the screen in a circle
    def move_monster_circle(self):
        for i in range(7):
            monster = self.circle_monsters[i]
            monster.rect.x = 640 + \
                math.cos(monster.velocity + 2 * math.pi * i / 10) * \
                self.radius - monster.width / 2
            monster.rect.y = 315 + \
                math.sin(monster.velocity + 2 * math.pi * i / 10) * \
                self.radius - monster.width / 2
            monster.velocity += self.circle_velocity

    # To create the monsters on the right side of the screen
    def monsters_right(self):
        starting_xy = [(1160, 0), (1000, 608)]
        self.right_monsters = []
        for i in range(2):
            monster = self.new_monster()
            monster.rect.x = starting_xy[i][0]
            monster.rect.y = starting_xy[i][1]
            if i != 0 and i & 2 == 0:
                monster.velocity = -monster.velocity
            self.right_monsters.append(monster)

    # To move the monsters on the right side of the screen
    def move_right_monsters(self):
        for i in range(2):
            monster = self.right_monsters[i]
            monster.rect.y += monster.velocity
            if monster.rect.y <= 0:
                monster.velocity = -monster.velocity
            if monster.rect.y >= 608:
                monster.velocity = -monster.velocity

    # To create a new monster
    def new_monster(self):
        monster = Monster(self.images[2], self.event_listener)
        return monster

    # To check if the player touches a monster or a coin
    def check_collision(self):
        # To stop the game and display the game over message when the player touches a monster
        for i in range(len(self.left_monsters)):
            if self.robot.rect.colliderect(self.left_monsters[i].rect):
                self.game_over = True
        for i in range(len(self.circle_monsters)):
            if self.robot.rect.colliderect(self.circle_monsters[i].rect):
                self.game_over = True
        for i in range(len(self.right_monsters)):
            if self.robot.rect.colliderect(self.right_monsters[i].rect):
                self.game_over = True

        # To increase the points and put the coin in a new location when the player collects a coin
        if self.robot.rect.colliderect(self.coin.rect):
            self.points += 1
            position = random.randint(0, len(self.coin_positions) - 1)
            self.coin.rect.x = self.coin_positions[position][0]
            self.coin.rect.y = self.coin_positions[position][1]

            # To increase the speed of the monsters if they are not yet at their maximum speed
            if self.go_faster:
                self.increase_velocity()

    # To randomly pick a group of monsters and increase their speed
    def increase_velocity(self):
        choice = random.randint(1, 3)
        if choice == 1 and self.left_counter < 3:
            for monster in self.left_monsters:
                monster.velocity *= 1.3
            self.left_counter += 1
        if choice == 2 and self.circle_counter < 5:
            for monster in self.circle_monsters:
                self.circle_velocity += 0.001
            self.circle_counter += 1
        if choice == 3 and self.right_counter < 7:
            for monster in self.right_monsters:
                monster.velocity *= 1.3
            self.right_counter += 1

        # To stop the monsters from going to fast and making it impossible to not touch them
        if self.left_counter + self.circle_counter + self.right_counter == 15:
            self.go_faster = False

    # The main loop of the game where all the other functions are called
    def main_loop(self):
        while True:
            self.event_listener.check_events()
            self.check_collision()
            self.draw_window()
            if not self.game_over:
                self.robot.move()
                self.move_left_monsters()
                self.move_monster_circle()
                self.move_right_monsters()
            if self.event_listener.start_new:
                self.event_listener.start_new = False
                self.new_game()

    # To draw the game window
    def draw_window(self):
        self.window.fill((62, 48, 45))
        # Robot
        self.window.blit(self.robot.image, self.robot.rect)
        # Bottom of screen
        pygame.draw.rect(self.window, (53, 54, 56), (0, 680, 1280, 40))
        # Left wall
        pygame.draw.line(self.window, (137, 143, 137),
                         (350, 0), (350, 550), width=6)
        # Right wall
        pygame.draw.line(self.window, (137, 143, 137),
                         (920, 130), (920, 680), width=6)
        # Monsters on the left
        for i in range(3):
            monster = self.left_monsters[i]
            self.window.blit(monster.image, monster.rect)
        # Circle of monsters
        for i in range(7):
            monster = self.circle_monsters[i]
            self.window.blit(monster.image, monster.rect)
        # Monsters on the right
        for i in range(2):
            monster = self.right_monsters[i]
            self.window.blit(monster.image, monster.rect)
        # Coin
        self.window.blit(self.coin.image, self.coin.rect)
        # Text on Bottom of Screen
        text_coins = self.game_font.render(
            f"Coins: {self.points}", True, (137, 143, 137))
        self.window.blit(text_coins, (50, 685))
        text_new = self.game_font.render(
            "F2 = new game", True, (137, 143, 137))
        self.window.blit(text_new, (850, 685))
        text_exit = self.game_font.render(
            "Esc = exit game", True, (137, 143, 137))
        self.window.blit(text_exit, (1050, 685))

        # Text to display if the game is over
        if self.game_over:
            # Text to be displayed depending on the number of coins the player collected
            text_game_over = self.game_over_font.render(
                "-= GAME OVER =-", True, (137, 143, 137))
            if self.points < 1:
                text_end = self.game_font.render(
                    "You collected 0 coins. Avoid the Ghosts and collect as many coins as you can!", True, (137, 143, 137))
            elif self.points == 1:
                text_end = self.game_font.render(
                    f"You have 1 coin! Try to Collect more next Time!", True, (137, 143, 137))
            elif self.points > 1:
                text_end = self.game_font.render(
                    f"Congratulations, you have {self.points} coins! Collect even more next Time!", True, (137, 143, 137))
            text_again = self.game_font.render(
                "Press F2 to try again or ESC to quit.", True, (137, 143, 137))

            # To center the different text snippets
            text_end_x = 1280 / 2 - text_end.get_width() / 2
            text_end_y = 720 / 2 - text_end.get_height() / 2
            text_game_over_x = 1280 / 2 - text_game_over.get_width() / 2
            text_game_over_y = (720 / 2 - text_game_over.get_height() / 2) - 50
            text_again_x = 1280 / 2 - text_again.get_width() / 2
            text_again_y = (720 / 2 - text_again.get_height() / 2) + 50

            # To draw a rectangle around the text
            pygame.draw.rect(self.window, (53, 54, 56), (text_game_over_x,
                             text_game_over_y, text_game_over.get_width(), text_game_over.get_height()))
            pygame.draw.rect(self.window, (53, 54, 56), (text_end_x,
                             text_end_y, text_end.get_width(), text_end.get_height()))
            pygame.draw.rect(self.window, (53, 54, 56), (text_again_x,
                             text_again_y, text_again.get_width(), text_again.get_height()))

            # To display the text
            self.window.blit(
                text_game_over, (text_game_over_x, text_game_over_y))
            self.window.blit(text_end, (text_end_x, text_end_y))
            self.window.blit(text_again, (text_again_x, text_again_y))

        # To draw everything at 60 FPS
        pygame.display.flip()
        self.clock.tick(60)


class EventListener:  # To listen to the games events

    # Necessary variables to control the players movement and interaction with other objects
    def __init__(self):
        self.to_left = False
        self.to_right = False
        self.up = False
        self.down = False
        self.start_new = False

    # Loop that listens for events
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_DOWN:
                    self.down = True
                if event.key == pygame.K_F2:
                    self.start_new = True
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_UP:
                    self.up = False
                if event.key == pygame.K_DOWN:
                    self.down = False


class Character:  # Parrent class for the characters in the game
    # To initialize the object with all necessary variables
    def __init__(self, image: str, eventlistener: EventListener):
        self.image = image
        self.velocity = 2
        self.rect = pygame.Rect(0, 0, 40, 60)
        print(self.rect)
        self.eventlistener = eventlistener
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class Player(Character):  # Subclass for the players character
    # Additional variabels necessary for the player
    def __init__(self, image: str, name: str, player_x: int, player_y: int, eventlistener: EventListener):
        super().__init__(image, eventlistener)
        self.name = name
        self.velocity = 4
        self.rect.x = player_x
        self.rect.y = player_y

    # To move the player but not let him move through walls
    def move(self):
        # To move to the left
        if self.eventlistener.to_left == True:
            if self.rect.x >= 920 and self.rect.x < 1238:
                self.rect.x -= self.velocity
            elif self.rect.x >= 350 and self.rect.y <= 46:
                self.rect.x -= self.velocity
            elif self.rect.x < 877 and self.rect.x >= 350:
                self.rect.x -= self.velocity
            elif self.rect.x < 877 and self.rect.x > 0 and self.rect.y >= 550:
                self.rect.x -= self.velocity
            elif self.rect.x < 306 and self.rect.x > 0:
                self.rect.x -= self.velocity

        # To move to the right
        if self.eventlistener.to_right == True:
            if self.rect.x <= 300:
                self.rect.x += self.velocity
            elif self.rect.x <= 872 and self.rect.y >= 550:
                self.rect.x += self.velocity
            elif self.rect.x <= 872 and self.rect.x > 347:
                self.rect.x += self.velocity
            elif self.rect.x > 384 and self.rect.x < 1236 and self.rect.y <= 46:
                self.rect.x += self.velocity
            elif self.rect.x > 915 and self.rect.x < 1236:
                self.rect.x += self.velocity
        
        # To move up
        if self.eventlistener.up == True:
            if self.rect.y > 0 and self.rect.x not in range(304, 348):
                self.rect.y -= self.velocity

        # To move down
        if self.eventlistener.down == True:
            if self.rect.y < 680 - self.height and self.rect.x not in range(874, 916):
                self.rect.y += self.velocity


class Monster(Character): # A seperate class for the monsters
    # Additional variabels necessary for the monsters
    def __init__(self, image: str, eventlistener: EventListener):
        super().__init__(image, eventlistener)
        self.rect.x = 0
        self.rect.y = 0


class Coin: # A class for the coin the player has to collect
    # Additional variabels necessary for the coin
    def __init__(self, image: str, eventlistener: EventListener):
        self.image = image
        self.rect = self.image.get_rect()
        self.eventlistener = eventlistener
        self.rect.x = 332
        self.rect.y = 600

# To start the game the code is not beeing tested
if __name__ == "__main__":
    Game()
