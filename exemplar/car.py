import pygame
white = (255, 255, 255)

class Car(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class
    # in Pygame.

    def __init__(self, colour, width, height, speed):
        # Call the parent class (Sprite) constructor.
        super().__init__()

        # Create the background surface and set it to be transparent.
        # Pass in the colour of the car, and its x and y position, 
        # width and height.
        
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)

        # Initialise attributes of the car.
        self.width = width
        self.height = height
        self.colour = colour
        self.speed = speed

        # Draw the car (a rectangle).
        pygame.draw.rect(self.image, self.colour, [0, 0, self.width, 
        self.height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move_right(self, pixels, SCREEN_WIDTH):
        """ Moves car right, but only as will only allow the car to move
        to within 5 pixels of the edge of the screen (otherwise, the
        player can 'cheat' by going offscreen.
        """
        if self.rect.x < SCREEN_WIDTH - (self.width + 5):
            self.rect.x += pixels
        
    def move_left(self, pixels):
        """ Moves car left, but only as will only allow the car to move
        within 5 pixels of the edge of the screen (otherwise, the player
        can 'cheat' by going offscreen.
        """
        if self.rect.x > 5:
            self.rect.x -= pixels

    def move_forward(self, speed):
        """ Moves enemy cars down the screen, giving the
        illusion of the player car moving forward. The longer the up
        arrow is pressed, the faster the cars move (giving the illusion
        of the player car speeding up).
        """
        self.rect.y += self.speed * speed / 20


    def change_speed(self, speed):
        """Change the speed of the enemy cars.
        """
        self.speed = speed

    def repaint(self, colour):
        """Create a new sprite (car), based on a random colour (sent
        from the main module).
        """
        self.colour = colour
        pygame.draw.rect(self.image, self.colour, [0, 0, self.width,
                                                   self.height])