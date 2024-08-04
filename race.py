import pygame, random
import time
from threading import Timer

pygame.init()

width = 800

height = 600
speed = 8
bg = pygame.image.load('images/road.png')
car_sound = pygame.mixer.Sound('sounds/song.mp3')
bonus_sound = pygame.mixer.Sound('sounds/speed_up.mp3')
win_sound = pygame.mixer.Sound('sounds/win_sound.mp3')
game_over_sound = pygame.mixer.Sound('sounds/game_over.mp3')
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(new_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Car(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed):
        super().__init__(new_image, x, y, width, height)
        car_left = pygame.image.load('images/car2.png')
        car_left = pygame.transform.scale(car_left, (width, height))
        car_left = pygame.transform.rotate(car_left, 10)
        car_right = pygame.image.load('images/car3.png')
        car_right = pygame.transform.scale(car_right, (width, height))
        car_right = pygame.transform.rotate(car_right, -10)
        blue_image = pygame.image.load('images/car4.png')
        blue_image = pygame.transform.scale(blue_image, (width, height))
        blue_image_left = pygame.transform.rotate(blue_image, 10)
        blue_image_right = pygame.transform.rotate(blue_image, -10)
        self.cars_sprites = {
            'original': {
                'car_left': car_left,
                'car_right': car_right,
                'default': self.image
                },
            'boosted': {
                'car_left': blue_image_left,
                'car_right': blue_image_right,
                'default': blue_image
                }
            }
        self.key = 'original'
        self.current_image = self.cars_sprites[self.key]['default']
        self.original_rect = self.rect.copy()
        self.speed = speed
        self.collision = True
        self.bonus_timer = Timer(5, self.colission_return)
        self.enlarged = False
        self.enlarge_start_time = 0

    def colission_return(self):
        global speed
        speed = 8
        self.collision = True
        self.key = 'original'

    def start_bonus(self):
        global speed
        speed += 4
        self.collision = False
        self.key = 'boosted'
        if self.bonus_timer:
            self.bonus_timer.cancel()
            self.bonus_timer = Timer(5, self.colission_return)
        self.bonus_timer.start()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = self.cars_sprites[self.key]['car_left']
            return
        if keys[pygame.K_d] and self.rect.x < width - self.rect.width + 10:
            self.rect.x += self.speed
            self.image = self.cars_sprites[self.key]['car_right']
            return
        self.image = self.cars_sprites[self.key]['default']


class Obstacle(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed
        self.height = height

    def update(self):
        global speed
        self.rect.y += speed - 2
        if self.rect.y >= height + self.height:
            self.kill()

class Bonus(GameSprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__(new_image, x, y, width, height)
        self.height = height
    def update(self):
        global speed
        self.rect.y += speed + 1
        if self.rect.y >= height + self.height:
            self.kill()

class Human(GameSprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed
        self.height = height

    def update(self):
        global speed
        self.rect.y += speed + 1
        if self.rect.y >= + height + self.height:
            self.kill()

player = Car('images/car.png', width / 2, height - 170, 70, 130, 10)
people = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
coor_line = [160, 280, 400, 550]
new_coor_line = [10, 750]

obstacles_delay_time = 2
new_delay_time = 10
obstacles_last_spawn = 0
new_last_spawn = 0
new_last_spawn2 = 0
new_delay_time2 = 4
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.SysFont('Arial', 36)
label = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 40)
replay_label = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 25)
paused_label = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 40)
paused_label2 = pygame.font.Font('fonts/ofont.ru_Roboto.ttf', 30)
paused_text = ''
finish_text = font.render('Game Over', True, (255, 0, 0))
replay_text = font.render('Press R to Replay', True, (255, 255, 255))
won_text = font.render('Congratulations. You have won!', True, (3, 7, 252))
goal_text = font.render('Вы должны продержаться 100 секунд. Удачи!', True, (3, 7, 252))
finish = False
pause = False
win = False

def countdown():
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        countdown_text = font.render(str(i), True, (255, 255, 255))
        screen.blit(countdown_text, (screen.get_width() // 2 - countdown_text.get_width() // 2, screen.get_height() // 2 - countdown_text.get_height() // 2))
        screen.blit(goal_text, (0, 0))
        pygame.display.flip()
        time.sleep(1)

exit = False
car_collision = True
bg_y = 0
countdown()
start_ticks = pygame.time.get_ticks()
elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_m:
                game_over_sound.play()
            if event.key == pygame.K_p:
                pause = not pause
            if event.key == pygame.K_r and finish or win:
                obstacles.empty()
                people.empty()
                bonuses.empty()
                start_ticks = pygame.time.get_ticks()
                elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
                finish = False
                pause = True
                win = False
    if elapsed_seconds == 100:
        win = True
        win_sound.play()

    if pygame.sprite.spritecollide(player, obstacles, False) and player.collision:
        finish = True
        game_over_sound.play()
        obstacles.empty()
        finish_text = label.render('Вы проиграли!', False, (193, 196, 199))
        replay_text = replay_label.render('Нажмите R, что бы начать заново', False, (193, 196, 199))
    if pygame.sprite.spritecollide(player, people, False):
        finish = True
        game_over_sound.play()
        finish_text = label.render('Вы проиграли!', False, (193, 196, 199))
        replay_text = replay_label.render('Нажмите R, что бы начать заново', False, (193, 196, 199))
    if pygame.sprite.spritecollide(player, bonuses, True):
        player.start_bonus()
        bonus_sound.play()

    if time.time() - obstacles_last_spawn > obstacles_delay_time:
        obstacles_last_spawn = time.time()
        if not pause:
            for _ in range(random.randint(1, 3)):
                obstacles.add(Obstacle('images/enemy.png', random.choice(coor_line), 0 - 100, 50, 115, 5))
    if time.time() - new_last_spawn > new_delay_time:
        new_last_spawn = time.time()
        for i in range(1):
            bonuses.add(Bonus('images/bonus.png', random.randint(20, 750), 0 - 100, 40, 40))
    if time.time() - new_last_spawn2 > new_delay_time2:
        new_last_spawn2 = time.time()
        for d in range(1):
            people.add(Human('images/human.png', random.choice(new_coor_line), 0 - 100, 80, 80))


    if not pause and not finish:
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        print(speed)
        bg_y += speed
        if bg_y >= 600:
            bg_y = 0
        obstacles.update()
        bonuses.update()
        player.update()
        people.update()
        car_sound.play()
    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - 600))
    player.show()
    obstacles.draw(screen)
    people.draw(screen)
    bonuses.draw(screen)
    timer_text = font.render(f'Time: {elapsed_seconds}', True, (255, 255, 255))
    screen.blit(timer_text, (screen.get_width() - 150, 25))

    if finish:
        screen.fill((87, 88, 89))
        screen.blit(finish_text, (280, 250))
        screen.blit(replay_text, (230, 300))
        car_sound.stop()
        player.kill()
        player = Car('images/car.png', width / 2, height - 170, 70, 130, 10)
        # game_over_sound.play()

    if win:
        screen.fill((82, 252, 3))
        screen.blit(won_text, (170, 250))
        screen.blit(replay_text, (230, 300))
        car_sound.stop()
        player.kill()
        player = Car('images/car.png', width / 2, height - 170, 70, 130, 10)
        obstacles.empty()
        # win_sound.play()

    if pause:
        paused_text = paused_label.render('Paused', False, (193, 196, 199))
        paused_text2 = paused_label2.render('Press "p" to continue', False, (193, 196, 199))
        screen.blit(paused_text2, (260, 100))
        screen.blit(paused_text, (330, 230))
        car_sound.stop()
    pygame.display.update()
    clock.tick(60)