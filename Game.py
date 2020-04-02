import pygame
import random

from Raycasting import Raycasting

class Player(object):
    def __init__(self, x, y, vel, size):
        self.x = x
        self.y = y

        self.vel = vel

        self.size = size

        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

        self.score = 0

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.size[0], self.size[1]))

    def get_obj_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def kill(self):
        self.score = 0

    def setBounds(self, win_size, cur_x, cur_y, selection):
        new_x = cur_x
        new_y = cur_y

        if selection == 'wrap':
            if cur_x >= win_size[0]:
                new_x = 0
            if cur_x <= 0:
                new_x = win_size[0]

            if cur_y >= win_size[1]:
                new_y = 0
            if cur_y <= 0:
                new_y = win_size[1]

        if selection == 'fixed':
            if cur_x >= win_size[0] - self.size[0]:
                new_x = win_size[0] - self.size[0]
            if cur_x <= 0:
                new_x = 0

            if cur_y >= win_size[1] - self.size[1]:
                new_y = win_size[1] - self.size[1]
            if cur_y <= 0:
                new_y = 0

        return new_x, new_y

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel
        if keys[pygame.K_d]:
            self.x += self.vel

        self.x, self.y = self.setBounds((500, 500), self.x, self.y, 'fixed')

class Bar(object):
    def __init__(self, gap_size, win_width, win_height, vel):
        self.gap = gap_size

        self.win_width = win_width
        self.win_height = win_height

        self.vel = vel

        self.bar_height = 10

        self.l_x = self.l_y = self.r_y = self.r_width = self.r_x = 0
        self.l_width = random.randint(50, (self.win_width - 50 - self.gap))

        rect_left = self.l_width
        rect_top = self.l_y
        rect_width = self.gap
        rect_height = self.bar_height

        self.rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)
        self.left_rect = pygame.Rect(0, self.l_y, self.l_width, rect_height)
        self.right_rect = pygame.Rect((rect_left + rect_width), self.l_y, (self.win_width - (rect_left + rect_width)), rect_height)

        self.player_passed = False
        self.test_flag = False

        self.image = pygame.Surface((self.win_width, 10))

    def draw(self, win):
        # Left Bar Dims
        self.l_x = 0

        # Right Bar Dims
        self.r_x = self.l_width + self.gap
        self.r_y = self.l_y

        self.r_width = self.win_width - self.r_x

        pygame.draw.rect(win, (255, 0, 0), (self.l_x, self.l_y, self.l_width, self.bar_height))
        pygame.draw.rect(win, (255, 0, 0), (self.r_x, self.r_y, self.r_width, self.bar_height))

    def get_obj_rect(self):
        rect_left = self.l_width
        rect_top = self.l_y
        rect_width = self.gap
        rect_height = self.bar_height

        self.rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)
        self.left_rect = pygame.Rect(0, self.l_y, self.l_width, rect_height)
        self.right_rect = pygame.Rect((rect_left + rect_width), self.l_y, (self.win_width - (rect_left + rect_width)),
                                      rect_height)

    def collision_check_score(self, player):
        return self.rect.colliderect(player.rect)

    def collision_check_kill(self, player):
        return self.left_rect.colliderect(player.rect), self.right_rect.colliderect(player.rect)


class GameWindow:
    def __init__(self):

        self.width = 500
        self.height = 500

        self.size = (self.width, self.height)

        self.win = pygame.display.set_mode(self.size)
        pygame.display.set_caption("AI Bar Game")

        self.player = Player(250, 250, 3, (10, 10))

        self.game_time = 0
        self.game_refresh = 10

        self.run = True

        self.bar_gap = 100
        self.bar_vel_initial = 2
        self.bar_vel = 0
        self.bars = []

        self.passed_though_bars = False
        self.previous_collision = False
        self.score_list = [0, 0]

        self.score_font = pygame.font.SysFont('Comic Sans MS', 32)
        self.score_text_surface = self.score_font.render('Score: 0', False, (255, 255, 255))

        self.raycasting = Raycasting(self.win, (self.player.x, self.player.y))

        self.bar_gap_coords = []

        self.ray_distances = []

    def re_init(self):
        self.player = Player(250, 250, 3, (10, 10))

        self.game_time = 0
        self.game_refresh = 10

        self.run = True

        self.bar_gap = 100
        self.bar_vel_initial = 1
        self.bar_vel = 0
        self.bars = []

        self.passed_though_bars = False
        self.previous_collision = False
        self.score_list = [0, 0]

    def draw(self):

        self.win.fill((0, 0, 0))

        self.win.blit(self.score_text_surface, (0, 0))

        self.player.draw(self.win)

        for bar in self.bars:
            bar.draw(self.win)

        self.raycasting.draw()

        self.score_text_surface = self.score_font.render('Score: {}'.format(self.player.score), False, (255, 255, 255))


        pygame.display.update()

    def getScore(self, bar):
        self.score_list.append(bar.collision_check(self.player))
        self.score_list.pop(0)

        if self.score_list[0] == 1 and self.score_list[1] == 0:
            self.player.score += 1


    def run_game(self):

        while self.run:
            print("Start")
            pygame.time.delay(self.game_refresh)
            self.passed_though_bars = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.ray_distances = []

            self.bar_vel = self.bar_vel_initial + (self.game_time / 10000)

            if self.game_time % 700 == 0:
                self.bars.append(Bar(self.bar_gap, self.width, self.height, self.bar_vel))

            self.bar_gap_coords = []

            for bar in self.bars:
                kill_player_left, kill_player_right = 0, 0

                if 500 >= bar.l_y >= 0:
                    bar.l_y += bar.vel
                else:
                    self.bars.pop(self.bars.index(bar))

                bar.get_obj_rect()

                self.bar_gap_coords.append(((int(bar.l_x), int(bar.l_y)), (int(bar.l_width + bar.l_x), int(bar.l_y))))
                self.bar_gap_coords.append(((int(bar.r_x), int(bar.r_y)), (int(bar.r_width + bar.r_x), int(bar.r_y))))

                self.player.get_obj_rect()
                if bar.collision_check_score(self.player):
                    bar.player_passed = True

                kill_player_left, kill_player_right = bar.collision_check_kill(self.player)

                if kill_player_left or kill_player_right:
                    self.player.kill()
                    self.re_init()

                if not bar.test_flag:

                    if bar.player_passed:
                        self.player.score += 1
                        bar.player_passed = False
                        bar.test_flag = True

            self.draw()

            self.player.update()
            self.obst_coord = [((0, 300), (150, 300)), ((0, 400), (50, 400)), ((150, 400), (500, 400)), ((250, 300), (500, 300))]
            self.raycasting.update((int(self.player.x + self.player.size[0] / 2), int(self.player.y + self.player.size[0] / 2)), self.bar_gap_coords)
            self.ray_distances = self.raycasting.dist
            print(self.ray_distances)

            self.game_time += self.game_refresh

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    gamewindow = GameWindow()
    gamewindow.run_game()
