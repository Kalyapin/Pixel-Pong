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


class MessageSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (450, 350))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Button(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (250, 250))
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
player_comp = AI("images/player2.png", 678, 250, 3)
ball = Ball("images/ball.png", 350, 250, 4)
letter_win = MessageSprite("images/win.png", 120, 0)
letter_lose = MessageSprite("images/letter_lose.png", 120, 0)
letter_pingPong = MessageSprite("images/ping_pong.png", 130, 0)
button_pp = Button("images/button_play_player.png", 220, 200)
button_pc = Button("images/button_play_comp.png", 220, 300)
loading = MessageSprite("images/loading.png", 120, 150)
back = Button("images/button_back.png", 220, 250)

play_variant = 0
# 1 - player
# 2 - AI

score = 0

clock = time.Clock()
fps = 60

state = 0
state_timer = 0
# 0 - menu
# 1 - load lvl
# 2 - win
# 3 - lose
# 4 - play comp
# 5 - play player

game = True
while game:
    window.blit(background, (0, 0))

    if state == 0:
        letter_pingPong.reset()
        button_pp.reset()
        button_pc.reset()


    if state == 1:
        loading.reset()
        if state_timer == 120 and play_variant == 1:
            state = 5
            state_timer = 0

        elif state_timer == 120 and play_variant == 2:
            state = 4
            state_timer = 0

        state_timer += 1

    if state == 2:
        letter_win.reset()
        back.reset()
        pass

    if state == 3:
        letter_lose.reset()
        back.reset()
        pass

    if state == 4:
        player1.update()
        player1.reset()
        player_comp.update()
        player_comp.reset()
        ball.update()
        ball.reset()
        play_variant = 2

        if ball.colliding_with(player1) or ball.colliding_with(player_comp):
            ball.reverse()

        if ball.rect.x > 700:
            score += 1
            state = 1
            ball.rect.x = 350
            print(score)

        elif score == 5:
            state = 2
            score = 0

        elif ball.rect.x < 10:
            score -= 1
            state = 1
            ball.rect.x = 350
            print(score)

        elif score == -5:
            state = 3
            score = 0

    if state == 5:
        play_variant = 1
        player1.update()
        player1.reset()
        player2.update()
        player2.reset()
        ball.update()
        ball.reset()

        if ball.colliding_with(player1) or ball.colliding_with(player2):
            ball.reverse()

        if ball.rect.x > 700:
            score += 1
            state = 1
            ball.rect.x = 350
            print(score)

        elif score == 5:
            state = 2
            score = 0

        elif ball.rect.x < 10:
            score -= 1
            state = 1
            ball.rect.x = 350
            print(score)

        elif score == -5:
            state = 3
            score = 0


    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            if button_pp.button_click(x, y) and state == 0:
                state = 1
            if button_pc.button_click(x, y) and state == 0:
                state = 4
            if back.button_click(x, y) and state == 2 or back.button_click(x, y) and state == 3:
                state = 0

    clock.tick(fps)
    display.update()
