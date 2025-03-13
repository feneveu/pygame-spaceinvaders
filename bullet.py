import pygame as pg


class Bullet(pg.sprite.Sprite):
    """Bullet shop by the ship"""
    def __init__(self, xpos, ypos):
        super().__init__()
        # sets up the images
        self.image = pg.image.load("images/laser.png").convert_alpha()
        # makes the bullets a mask so its hitbox becomes the image
        self.mask = pg.mask.from_surface(self.image)
        # creates the rectangle around the bullet
        self.rect = pg.Rect(xpos, ypos, self.image.get_width(), self.image.get_height())

        # sets the speed of the bullet
        self.speed = 100

    def update(self, dt):
        """moves the rectangle of the bullet"""
        self.rect.y -= self.speed * dt
        # if the ship bullet goes passed the ceiling it dies
        if self.rect.bottom < 0:
            self.die()

    def die(self):
        """a bullet must delete itself to die"""
        self.kill()
        del self


class EnemyLaser(pg.sprite.Sprite):
    """Enemy Laser"""
    def __init__(self, xpos, ypos):
        super().__init__()

        # renders an image for the enemy laser
        self.image = pg.image.load("images/enemylaser.png").convert_alpha()
        # creates a mask for the laser
        self.mask = pg.mask.from_surface(self.image)
        # creates the rectangle around the image
        self.rect = pg.Rect(xpos, ypos, self.image.get_width(), self.image.get_height())

        # sets the speed of the bullets falling
        self.speed = 100

    def update(self, dt):
        """updates the position of the laser"""
        self.rect.y += self.speed * dt

        # if it goes under the screen the lasers die
        if self.rect.top > 600:
            self.die()

    def die(self):
        """kills the laser"""
        self.kill()
        del self
