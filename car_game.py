import pygame as pg
import random

pg.init()
pg.font.init()
clock = pg.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 800
FPS = 120
WINDOW = pg.display
WINDOW.set_caption("Car Racer")
WINDOW.set_icon(pg.image.load('assets/application/game_icon.png'))
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Background:
    def __init__(self):
        self.bg = pg.image.load('assets/environment/grass.png').convert_alpha()
        self.posy, self.speed = -700, 0

    def draw(self):
        self.posy += self.speed
        if self.posy >= 0:
            self.posy = -700
        SCREEN.blit(self.bg, (0, int(self.posy)))

class Player:
    def __init__(self):
        self.image_straight = pg.image.load('assets/cars/car_1.png').convert_alpha()
        self.image_left = pg.image.load('assets/cars/car_1.png').convert_alpha()
        self.image_right = pg.image.load('assets/cars/car_1.png').convert_alpha()
        self.image = self.image_straight
        self.trace = (0, 0, 0, 0)
        self.posx, self.posy, self.speed, self.carspeed = 315, 650, 0, -5
        self.moving_left, self.moving_right, self.gas, self.brake = False, False, False, False

    def move(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.gameover = True
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.moving_left = True
                elif event.key == pg.K_RIGHT:
                    self.moving_right = True
                elif event.key == pg.K_UP:
                    self.gas = True
                elif event.key == pg.K_DOWN:
                    self.brake = True
            if event.type == pg.KEYUP:
                self.moving_left, self.moving_right, self.gas, self.brake = False, False, False, False
        self.image = self.image_straight
        if self.moving_left and not self.posx - 2.5 <= 205:
            self.posx -= 2.5
            self.image = self.image_left
        if self.moving_right and not self.posx + 2.5 >= 440:
            self.posx += 2.5
            self.image = self.image_right
        if self.gas and self.speed < 300:
            self.speed += 1/3
            bg.speed += .05/3
            flag.speed += .005/3
            self.carspeed += .03/3
        if self.brake and self.speed > 0:
            self.speed -= 1*2
            bg.speed -= .05*2
            flag.speed -= .005*2
            self.carspeed -= .03*2
        if self.speed <= 0 or bg.speed <= 0:
            self.speed = 0
            bg.speed = 0
    
    def draw(self):
        self.trace = SCREEN.blit(self.image, (int(self.posx), int(self.posy)))
        self.trace = (self.trace[0]+5, self.trace[1]+5, self.trace[2]-10, self.trace[3]-10)

class Car:
    def __init__(self, posx):
        self.image0 = pg.image.load('assets/cars/car_2.png').convert_alpha()
        self.image1 = pg.image.load('assets/cars/car_3.png').convert_alpha()
        self.image2 = pg.image.load('assets/cars/car_4.png').convert_alpha()
        self.image3 = pg.image.load('assets/cars/car_5.png').convert_alpha()
        self.image4 = pg.image.load('assets/cars/car_6.png').convert_alpha()
        self.image_list = (self.image0, self.image1, self.image2, self.image3, self.image4)
        self.image = self.image_list[4]
        self.trace = (0, 0, 0, 0)
        self.posx, self.posy, self.speed = posx, -500, 0
        self.is_moving = False

    def move(self):
        if not self.is_moving:
            rnd = random.randint(1, game.difficulty)
            if rnd == 50:
                self.is_moving = True
                self.image = self.image_list[random.randint(0, 4)]
                self.speed = random.randint(0, 3)
        else:
            self.posy += player.carspeed + self.speed
            if self.posy >= SCREEN_HEIGHT or self.posy <= -999:
                self.is_moving = False
                self.posy = -150
    
    def draw(self):
        self.trace = SCREEN.blit(self.image, (int(self.posx), int(self.posy)))
        self.trace = (self.trace[0]+5, self.trace[1]+5, self.trace[2]-10, self.trace[3]-10)

class Flag:
    def __init__(self):
        self.image = pg.image.load('assets/environment/finish.png')
        self.trace = (0, 0, 0, 0)
        self.posx, self.posy, self.speed = 210, -999, 0
        self.is_moving = False

    def move(self):
        if not self.is_moving:
            self.is_moving = True
            self.posx = random.randint(205, 450)
        else: 
            self.posy += self.speed
            if self.posy >= SCREEN_HEIGHT:
                self.is_moving = False
                self.posy = -50
                game.difficulty -= 100
                if game.difficulty <= 100:
                    game.difficulty = 100
    
    def draw(self):
        self.trace = SCREEN.blit(self.image, (int(self.posx), int(self.posy)))

class Game:
    def __init__(self):
        self.score, self.gameover, self.difficulty = 0, False, 500
        self.FONT = pg.font.SysFont('arial', 20)
        self.image = pg.image.load('assets/environment/finish.png')

    def draw_score(self):
        txt_speed = self.FONT.render('Speed:' + str(int(player.speed)) + ' mph', True, (255, 255, 255))
        txt_score = self.FONT.render('Score:' + str(self.score), True, (255, 255, 255))
        SCREEN.blit(txt_speed, (10, 610))
        SCREEN.blit(txt_score, (10, 640))

    def collision(self):
        p = pg.Rect(player.trace)
        f = pg.Rect(flag.trace)
        cars = [pg.Rect(car1.trace), pg.Rect(car2.trace), pg.Rect(car3.trace), pg.Rect(car4.trace)]
        if p.colliderect(f):
            flag.posx = -50
            game.score += 1
        for car in cars:
            if p.colliderect(car):
                SCREEN.blit(self.image, (int(player.posx - 80), int(player.posy + 10)))
                WINDOW.update()
                pg.time.delay(5000)
                self.gameover = True
    
    def mainloop(self):
        while not self.gameover:
            clock.tick(FPS)
            bg.draw()
            flag.move()
            flag.draw()
            player.move()
            player.draw()
            car1.move()
            car1.draw()
            car2.move()
            car2.draw()
            car3.move()
            car3.draw()
            car4.move()
            car4.draw()
            game.draw_score()
            game.collision()
            WINDOW.update()

bg = Background()
player = Player()
car1 = Car(posx=205)
car2 = Car(posx=280)
car3 = Car(posx=360)
car4 = Car(posx=435)
flag = Flag()
game = Game()

game.mainloop()
pg.quit()
quit()