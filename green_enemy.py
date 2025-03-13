import pygame as pg
from bullet import EnemyLaser


class GreenEnemy(pg.sprite.Sprite):

    def __init__(self, posx, posy, enemy_group):
        super(GreenEnemy, self).__init__()

        # sets up the images for the green enemy
        e3_1 = pg.image.load("images/enemy3_1.png").convert_alpha()
        e3_2 = pg.image.load("images/enemy3_2.png").convert_alpha()

        # changes the size of the image
        new_size = (e3_1.get_width() // 6.7, e3_1.get_height() // 6.7)  # Shrinks by 50%

        # creates a list that can toggle between images
        self.img_list = [
            pg.transform.scale(e3_1, new_size),
            pg.transform.scale(e3_2, new_size)
        ]

        # starts at the first image
        self.image = self.img_list[0]
        # creates a mask
        self.mask = pg.mask.from_surface(self.image)
        # sets a rectangle
        self.rect = pg.Rect(posx, posy, self.image.get_width(), self.image.get_height())

        # there have been 0 animation counts
        self.anim_counter = 0

        # the speed that they move at side to side
        self.speed = 35

        # will switch to number 1 as the other animation
        self.image_switch = 1

        # the x position of this specific alien
        self.xpos = posx
        # the y position of this specific alien
        self.ypos = posy

        # the green aliens are worth 10 points
        self.worth = 10

        # sets the laser enemy group
        self.lasers = enemy_group

    def toggle_image(self):
        """switches the image in animation"""
        if self.image_switch == 0:
            self.image_switch = 1
        else:
            self.image_switch = 0

    def update(self, dt):
        """updates the alien"""
        # after 8 'frames' toggle the image
        if self.anim_counter == 8:
            self.image = self.img_list[self.image_switch]
            self.toggle_image()
            self.anim_counter = 0
        self.anim_counter += 1

    def shoot(self):
        """makes the alien shoot"""

        # creates a laser, at the center of this specific alien
        b = EnemyLaser(self.rect.centerx, self.rect.top)
        # add this to the sprite group
        self.lasers.add(b)

    def die(self):
        """kills the alien"""
        self.kill()
        del self
