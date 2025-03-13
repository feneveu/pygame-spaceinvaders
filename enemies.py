import random
from green_enemy import GreenEnemy
from purple_enemy import PurpleEnemy
from blue_enemy import BlueEnemy
from mystery_enemy import MysteryEnemy
import time
import pygame as pg


class Enemies:
    """controls the array of enemies"""
    def __init__(self, enemy_group):
        # start of the enemy matrix
        self.row = []

        # sets the direction of the characters
        self.direction = -1
        # sets the direction of the mystery enemy
        self.mysdirection = -1

        # this is the enemy group for the enemies
        self.enemies = enemy_group

        # creates a sprite group for the enemy bullets
        self.enemy_bullets = pg.sprite.Group()

        # forces the shots to happen at different times
        self.last_shot_time = 0
        self.enemy_cooldown = 1.5

        # creates a random cool-down-time for the mys alien
        # (later - create a random stay on screen time)
        self.last_mys = 0
        self.mys_cool_down = self.random_mys()

    def random_mys(self):
        """random value for the cooldown"""
        value = random.choice([4, 5, 6, 7, 8, 9])
        return value

    def create_row(self, length, width, typed=1):
        """creates a row of critters"""

        # sets a random alien for each row
        if typed == 0:
            # sets the number of rows needed to fill the matrix
            for x in range(width):
                # the new row that will be added
                new_row = []

                # selects a random value that will be the type of alien chosen
                randval = random.randint(1, 3)
                # this is the position x which is relative to the size of the row and screen
                posx = 600/length
                # y position is based on number of rows already in the matrix
                posy = (len(self.row) + 1)*50

                # goes through the individual rows and adds aliens
                for i in range(0, length):
                    # if its 1, Green Aliens are created
                    if randval == 1:
                        # add it and move the x position for new alien
                        e = GreenEnemy(posx, posy, self.enemy_bullets)
                        new_row.append(e)
                        posx += e.image.get_width() + 15
                        self.enemies.add(e)
                    # if its 2, Purple Alien
                    elif randval == 2:
                        e = PurpleEnemy(posx, posy, self.enemy_bullets)
                        new_row.append(e)
                        posx += e.image.get_width() + 15
                        self.enemies.add(e)
                    # if its 3, Blue Alien
                    elif randval == 3:
                        e = BlueEnemy(posx, posy, self.enemy_bullets)
                        new_row.append(e)
                        posx += e.image.get_width() + 15
                        self.enemies.add(e)

                # add this new row to the matrix
                self.row.append(new_row)

        # layered by point value/ like og game w/mystery alien
        else:
            # sets the rows to none and make sure layout is correct
            self.row = []

            # create a mystery alien
            mys = MysteryEnemy(300, 50)
            # append the mystery alien to the matrix
            row1 = [mys]
            self.row.append(row1)
            self.enemies.add(mys)

            # add a row of 40pt Purple Aliens
            row2 = []
            posx = 600 / length
            posy = (len(self.row) + 1) * 50
            for i in range(length):
                e = PurpleEnemy(posx, posy, self.enemy_bullets)
                row2.append(e)
                posx += e.image.get_width() + 15
                self.enemies.add(e)
            self.row.append(row2)

            # add 2 rows of 20 point Blue Aliens
            posy = (len(self.row) + 1) * 50
            posx = 600 / length
            for x in range(2):
                row3 = []
                for i in range(length):
                    e = BlueEnemy(posx, posy, self.enemy_bullets)
                    row3.append(e)
                    posx += e.image.get_width() + 15
                    self.enemies.add(e)
                self.row.append(row3)
                posy = (len(self.row) + 1) * 50
                posx = 600 / length

            # add 2 rows of 10 pt Green Aliens
            posx = 600 / length
            for x in range(2):
                row4 = []
                for i in range(length):
                    e = GreenEnemy(posx, posy, self.enemy_bullets)
                    row4.append(e)
                    posx += e.image.get_width() + 15
                    self.enemies.add(e)
                self.row.append(row4)
                posx = 600 / length
                posy = (len(self.row) + 1) * 50

    def move(self, dt, window):
        """moves the aliens & fires shots"""
        # sets a timer so shots are fired at different intervals
        current_time = time.time()
        if current_time - self.last_shot_time > self.enemy_cooldown:
            rand_val = random.randint(1, 2)
            # tries to include randomness to each shot
            if rand_val == 1:
                self.shot()
                self.last_shot_time = current_time

        # go through each row
        for row in self.row:
            # if the row in nonempty there are aliens to move
            if len(row) != 0:
                # check the left edge of the alien and make sure it doesn't leave the window
                if row[0].rect.left <= 10:
                    # if this is a mystery alien, change the direction based on its individual speed
                    if isinstance(row[0], MysteryEnemy):
                        self.mysdirection = -1
                    # else change the direction based on the slower alien's speed
                    else:
                        self.direction = -1
                # check the right side, and differentiate between mystery and non-mystery
                elif row[-1].rect.right > 590:
                    if isinstance(row[0], MysteryEnemy):
                        self.mysdirection = 1
                    else:
                        self.direction = 1

                # iterate through enemies and deal with visibility
                for enemy in row:
                    # if it's a mystery alien
                    if isinstance(enemy, MysteryEnemy):
                        # makes the random choice/length of time for the mystery alien to stay on screen
                        random_gain = random.choice([4, 5, 6, 7, 8, 9, 10])

                        # creates the timer
                        current_time = time.time()
                        if current_time - self.mys_cool_down > self.last_mys:
                            # draws the mystery alien
                            enemy.rect.x -= enemy.speed * dt * self.mysdirection
                            enemy.xpos -= enemy.speed * dt * self.mysdirection
                            enemy.update(dt)
                            window.blit(enemy.image, enemy.rect)
                        # extends the aliens image on screen
                        if current_time - self.mys_cool_down > self.last_mys + self.mys_cool_down + random_gain:
                            self.last_mys = current_time

                    else:
                        # draws all other aliens
                        enemy.rect.x -= enemy.speed * dt * self.direction
                        enemy.xpos -= enemy.speed * dt * self.direction
                        enemy.update(dt)
                        window.blit(enemy.image, enemy.rect)

    def shot(self):
        """random alien shoots"""
        # pick a random available alien and make it shoot
        available_enemies = [enemy for row in self.row for enemy in row if enemy.alive()]
        if available_enemies:
            shooter = random.choice(available_enemies)
            if not isinstance(shooter, MysteryEnemy):
                shooter.shoot()

    def remove(self, enemy):
        """removes a specific alien from the matrix"""
        for row in self.row:
            if enemy in row:
                row.remove(enemy)
