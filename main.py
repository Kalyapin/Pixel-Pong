from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (40, 150))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def colliding_with(self, other_sprite):
        return sprite.collide_rect(self, other_sprite)

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Player1(GameSprite):
    def update(self):

        key_pressed = key.get_pressed()

        if key_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 345:
            self.rect.y += self.speed


class Player2(GameSprite):
    def update(self):

        key_pressed = key.get_pressed()

        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 345:
            self.rect.y += self.speed


class AI(GameSprite):
    def update(self):
        if self.rect.y < ball.rect.y and self.rect.y < 345:
            self.rect.y += self.speed
        elif self.rect.y > ball.rect.y and self.rect.y > 5:
            self.rect.y -= self.speed


class Ball(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (20, 20))
        self.speedx = player_speed
        self.speedy = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reverse(self):
        self.speedx *= -1

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.y > 490 or self.rect.y < 0:
            self.speedy *= -1

    def colliding_with(self, other_sprite):
        return sprite.collide_rect(self, other_sprite)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y


class MessageSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (350, 150))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class ScoreNumber(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (115, 150))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Button(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (250, 200))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def button_click(self, x, y):
        if self.rect.x < x < self.rect.x + 256 and self.rect.y < y < self.rect.y + 100:
            return True
        return False


window = display.set_mode((700, 500))
display.set_caption("Pixel Pong")
background = transform.scale(image.load("images/background2.png"), (700, 500))
player1 = Player1("images/player1.png", 2, 250, 3)
player2 = Player2("images/player2.png", 678, 250, 3)
ball = Ball("images/ball.png", 350, 250, 4)
letter_pingPong = MessageSprite("images/ping_pong.png", 160, 80)
button_pp = Button("images/button_play_player.png", 220, 200)
button_pc = Button("images/button_play_comp.png", 220, 300)
loading = MessageSprite("images/loading.png", 160, 150)
back = Button("images/button_back.png", 220, 250)
player1_win = MessageSprite("images/winner_player1.png", 160, 80)
player2_win = MessageSprite("images/winner_player2.png", 160, 80)

symbol = ScoreNumber("images/symbol_-.png", 300, 200)

images_score_left = [transform.scale(image.load("images/number_0.png"), (115, 150)),
                     transform.scale(image.load("images/number_1.png"), (115, 150)),
                     transform.scale(image.load("images/number_2.png"), (115, 150)),
                     transform.scale(image.load("images/number_3.png"), (115, 150)),
                     transform.scale(image.load("images/number_4.png"), (115, 150)),
                     transform.scale(image.load("images/number_5.png"), (115, 150))]

images_score_right = [transform.scale(image.load("images/number_0.png"), (115, 150)),
                     transform.scale(image.load("images/number_1.png"), (115, 150)),
                     transform.scale(image.load("images/number_2.png"), (115, 150)),
                     transform.scale(image.load("images/number_3.png"), (115, 150)),
                     transform.scale(image.load("images/number_4.png"), (115, 150)),
                     transform.scale(image.load("images/number_5.png"), (115, 150))]

score_left = 0
score_right = 0

clock = time.Clock()
fps = 60

state = 0
state_timer = 0
# 0 - menu
# 1 - load lvl
# 2 - win1
# 3 - win2
# 4 - play
# 6 - goal

game = True
while game:
    window.blit(background, (0, 0))

    if state == 0:

        letter_pingPong.reset()
        button_pp.reset()
        button_pc.reset()


    if state == 1:
        loading.reset()

        if state_timer == 120:
            score_left = 0
            score_right = 0
            player1.move(2, 250)
            player2.move(678, 250)
            ball.move(350, 250)
            state = 4
            state_timer = 0


        state_timer += 1

    if state == 2:
        player1_win.reset()
        back.reset()


    if state == 3:
        player2_win.reset()
        back.reset()


    if state == 4:
        player1.update()
        player1.reset()
        player2.update()
        player2.reset()
        ball.update()
        ball.reset()


        if ball.colliding_with(player1) or ball.colliding_with(player2):
            ball.reverse()

        if ball.rect.x > 700:
            score_left += 1
            state = 6
            print(score_left)

        if ball.rect.x < 10:
            score_right += 1
            state = 6
            print(score_right)

    if state == 6:
        window.blit(images_score_left[score_left], (150, 200))
        window.blit(images_score_right[score_right], (450, 200))
        symbol.reset()

        

        if state_timer == 120:
            if score_left == 5:
                state = 2
                state_timer = 0

            elif score_right == 5:
                state = 3
                state_timer = 0

        if state_timer == 180:

            state = 4

            player1.move(2, 250)
            player2.move(678, 250)
            ball.move(350, 250)

            state_timer = 0

        state_timer += 1

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            if button_pp.button_click(x, y) and state == 0:
                player1 = Player1("images/player1.png", 2, 250, 3)
                player2 = Player2("images/player2.png", 678, 250, 3)
                state = 1
            if button_pc.button_click(x, y) and state == 0:
                player1 = Player1("images/player1.png", 2, 250, 3)
                player2 = AI("images/player2.png", 678, 250, 3)
                state = 1

            if back.button_click(x, y) and state == 2 or back.button_click(x, y) and state == 3:
                state = 0

    clock.tick(fps)
    display.update()
