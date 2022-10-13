# Import our modules.
import pygame, random

# Import the Car class (from the car module - car.py).
from car import Car

# Initialise Pygame library.
pygame.init()

# Set colour tuples for game.
# Green, grey, and white used to create 'race track' background.
# Red used for player car; other colours used for enemy cars.
# Black used for text (scores, etc).
green = (20, 255, 140)
grey = (210, 210 ,210)
white = (255, 255, 255)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
blue = (100, 100, 255)
black = (0,0,0)

# List for different cars - (different colour rectangles).
colour_list = (green, purple, yellow, cyan, blue)

# Constants for screen width and height.
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600

# Create screen, caption, and icon for game.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Car Racer")

game_icon = pygame.image.load("game_icon.png")
pygame.display.set_icon(game_icon)

# Creates variable for clock speed.
clock = pygame.time.Clock()

# Frame rate for game.
FPS = 60

# Font for game (to display scores and messages).
game_font = pygame.font.SysFont("Arial", 20)

# This will be a list that will contain all the sprites to use
# in the game.
all_sprites_list = pygame.sprite.Group()

# Create an instance of the Car class for the player's car.
# It sends the parameters red (car colour), 60 and 80 
# (dimensions for car), and 70 (car speed).
player_car = Car(red, 60, 80, 70)

def reset_player():
    """Sets initial coordinates for player_car position, as well as 
    initial car speed.
    """
    x = 160
    y = SCREEN_HEIGHT-60
    speed = 1 
    return x, y, speed

# Code that follows creates four different instances of the Car class
# to create car1, car2, car3, and car4, and set their coordinates.
# The speed for each car is set as a random value from 50 to 100.
car1 = Car(purple, 60, 80, random.randint(50,100))
car1.rect.x = 60
car1.rect.y = -100

car2 = Car(yellow, 60, 80, random.randint(50,100))
car2.rect.x = 160
car2.rect.y = -600

car3 = Car(cyan, 60, 80, random.randint(50,100))
car3.rect.x = 260
car3.rect.y = -300

car4 = Car(blue, 60, 80, random.randint(50,100))
car4.rect.x = 360
car4.rect.y = -900


# Add each car to a list of objects.
all_sprites_list.add(player_car)
all_sprites_list.add(car1)
all_sprites_list.add(car2)
all_sprites_list.add(car3)
all_sprites_list.add(car4)

# Create a container class to hold and manage all the car
# sprites (except for the player's car).
all_coming_cars = pygame.sprite.Group()
all_coming_cars.add(car1)
all_coming_cars.add(car2)
all_coming_cars.add(car3)
all_coming_cars.add(car4)

def load_high_score():
    """Checks if HI_score.txt file exists. If it doesn't, creates file
    and writes the value 0 to the file.
    Then it sets the variable named value as the value read from the 
    file and returns it.
    """
    try:
        hi_score_file = open("HI_score.txt", 'r')
    except:
      hi_score_file = open("HI_score.txt", 'w')
      hi_score_file.write("0")
    hi_score_file = open("HI_score.txt", 'r')
    value = hi_score_file.read()
    hi_score_file.close()
    return value

def update_high_score(score, high_score):
    """Checks whether current score is greater than high score and,
    if so, updates high score. Otherwise, high score is returned as
    updated high score."""
    if(int(score) > int(high_score)):
      return score
    else:
      return high_score

def display_scores(score, score_colour, hi_score):
    """Displays current score and high score throughhout the game."""

    # Current score:
    display_score = game_font.render("Score: " + str(score), True, 
    score_colour)
    screen.blit(display_score, (SCREEN_WIDTH-140,10))

    # High score:
    display_score = game_font.render("HIGH SCORE: " + str(hi_score), 
    True, score_colour)
    screen.blit(display_score, (10,10))

def save_high_score(high_score):
    """Saves the updated high score when the program is exited."""
    hi_score_file = open("HI_score.txt", 'w')
    hi_score_file.write(str(high_score))
    hi_score_file.close()

def check_quit():
    message ("Exit? (Q = exit, A = continue, R = reset)", 
    black)                
    pygame.display.update()
    return True

def message(msg, txt_colour):
    txt = game_font.render(msg, True, txt_colour)
    text_box = txt.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(txt, text_box)


def game_loop():
    """Main game loop"""
    # Variable for whether player wants to exit game.
    play_on = True
    # Variable to check if player wants to stop playing.
    leave_game = False

    # Creating and loading high_score
    high_score = load_high_score()
    score = 0

    # Gets starting coordinates and speed for player's car.
    player_car.rect.x, player_car.rect.y, speed = reset_player()

    while play_on:
        for event in pygame.event.get():
            # Handles what happens if the user presses the X button
            # on the game window, or presses the Esc key. Checks whether
            # they really want to quit, continue, or reset the game.
            if event.type == pygame.QUIT:
                leave_game = check_quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leave_game = check_quit()
                
            while leave_game:
                # If the user presses the X button again, the game
                # is exited. If they press R, the game is reset
                # (coordinates and speeds set for 'enemy cars' and
                # player car reset at starting position). If they press
                # A, the game continues, and if they press Q, the game
                # exits.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play_on = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            play_on = True
                            leave_game = False
                            score = 0
                            player_car.rect.x, player_car.rect.y, speed \
                            = reset_player()
                            # Sets random speed and y coordinate for 
                            # 'enemy cars'.
                            for car in all_coming_cars:
                                car.change_speed(random.randint(50,
                                100))
                                car.rect.y = -200 - car.rect.y
                        if event.key == pygame.K_a:
                            leave_game = False
                        if event.key == pygame.K_q:
                            play_on = False
                            leave_game = False
            # Save the high score.
            save_high_score(high_score)

        # Handles movement of car based on keyboard (arrow) input.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_car.move_left(5)
            elif event.key == pygame.K_RIGHT:
                player_car.move_right(5, SCREEN_WIDTH)
            elif event.key == pygame.K_UP:
                # If the up arrow is pressed, the speed is increased.
                speed += 0.05
            elif event.key == pygame.K_DOWN:
                # If the down arrow is pressed, the speed is decreased -
                # as long as the speed is at least 0.5. (Otherwise the
                # player's car would start to move too slowly, or even
                # move backwards.
                if speed > 0.5:
                    speed -= 0.05
          
        # Logic for game. Moves all cars (other than the player's car).
        # When a car's y coordinate is greater than the 
        # screen height (ie when it goes off the bottom of the screen), 
        # its speed is randomly set and it is repainted (ie recreated
        # as a new car).
        for car in all_coming_cars:
            car.move_forward(speed)
            if car.rect.y > SCREEN_HEIGHT:
                car.change_speed(random.randint(50,100))
                car.repaint(random.choice(colour_list))
                # Ensure new car is positioned off screen (at bottom) as start 
                # point.
                car.rect.y = -200 - SCREEN_HEIGHT
                score += 1


        # Check if there is a car collision.
        car_collision_list = pygame.sprite.spritecollide(player_car,
        all_coming_cars,False)

        # If there is a collision, the player is asked if they want to play
        # again and the score is reset to 0.
        for car in car_collision_list:
            print("Car crash!") # Included for testing.
            save_high_score(high_score)
            message("You crashed! (Q = exit, A = play again)", black)
            pygame.display.update()
            score = 0


            # Handles input from user as to whether they want to play again
            # or quit. If they want to play again (A), the enemy car and 
            # player cars are 'reset'.
            leave_game = True
            while leave_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play_on = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            leave_game = False
                            player_car.rect.x, player_car.rect.y,speed\
                            = reset_player()
                            for car in all_coming_cars:
                                car.change_speed(random.randint(50,100))
                                car.rect.y = -200 - car.rect.y
                        if event.key == pygame.K_q:
                            play_on = False
                            leave_game = False

        # Updates the all_sprites_list list.
        all_sprites_list.update()

        # Background colour for screen.
        screen.fill(green)
        # Creates a rectangle representing the road.
        pygame.draw.rect(screen, grey, [40,0, 400,SCREEN_HEIGHT])
        # Creates line on road.
        pygame.draw.line(screen, white, [140,0],[140,SCREEN_HEIGHT],5)
        # Creates line on road.
        pygame.draw.line(screen, white, [240,0],[240,SCREEN_HEIGHT],5)
        # Creates line on road.
        pygame.draw.line(screen, white, [340,0],[340,SCREEN_HEIGHT],5)

        # Draw all the sprites at once. 
        all_sprites_list.draw(screen)

        # Update and display score and high score.
        high_score = update_high_score(score,high_score)
        display_scores(score, black, high_score)
        
        # Update the screen.
        pygame.display.update()

        # Frames rate for game.
        clock.tick(FPS)

    pygame.quit()
    quit()