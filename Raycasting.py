import pygame
import math
import collections


class Raycasting():
    def __init__(self, window, player_coordinates):
        self.win = window

        self.ray_list = []

        self.game_player_x, self.game_player_y = player_coordinates

        self.circle_coordinates = []
        self.ray_line_draw = []

        self.mouse_x, self.mouse_y = player_coordinates

        self.circle_coordinates = []
        self.ray_line_draw = []

    def ray(self, p_x, p_y, c_x, c_y):

        d_x = -p_x + c_x
        d_y = -p_y + c_y

        if d_x > 0:
            rad_x = math.atan(d_y/d_x)
        elif d_x < 0 and d_y >= 0:
            rad_x = math.atan(d_y/d_x) + math.pi
        elif d_x < 0 and d_y < 0:
            rad_x = math.atan(d_y/d_x) - math.pi
        elif d_x == 0 and d_y > 0:
            rad_x = math.pi/2
        elif d_x == 0 and d_y < 0:
            rad_x = -math.pi/2
        else:
            rad_x = rad_x = -math.pi/2

        line_length = 800
        end_y = p_y + (line_length * math.sin(rad_x))
        end_x = p_x + (line_length * math.cos(rad_x))

        return (p_x, p_y), (end_x, end_y)

    def draw_ray(self, pt_1, pt_2):
        pygame.draw.line(self.win, (255, 255, 255), pt_1, pt_2)

    def line(self, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])

        return A, B, -C

    def det(self, L1, L2):
        return L1[0] * L2[1] - L1[1] * L2[0]

    def find_line_dir(self, startpoint_coord, endpoint_coord):
        p_x, p_y = startpoint_coord
        e_x, e_y = endpoint_coord

        if e_x < p_x and e_y < p_y:
            dir = 'UL'
        if e_x > p_x and e_y < p_y:
            dir = 'UR'
        if e_x < p_x and e_y > p_y:
            dir = 'DL'
        if e_x > p_x and e_y > p_y:
            dir = 'DR'

        if e_x == p_x and e_y < p_y:
            dir = 'U'
        if e_x == p_x and e_y > p_y:
            dir = 'D'
        if e_x < p_x and e_y == p_y:
            dir = 'L'
        if e_x > p_x and e_y == p_y:
            dir = 'R'

        if e_x == p_x and e_y == p_y:
            dir = 'C'

        return dir

    def intersection(self, L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            return D, Dx, Dy
        else:
            return False

    def generate_int_point(self, int_det, ray_start_coord, ray_end_coord):
        D, Dx, Dy = int_det

        line_1_dir = self.find_line_dir(ray_start_coord, ray_end_coord)
        line_2_dir = self.find_line_dir(ray_start_coord, (Dx / D, Dy / D))

        if line_1_dir == line_2_dir:
            x = Dx / D
            y = Dy / D

            return x, y
        else:
            return (0, 0)

    def get_closest_intersection(self, intersection_line, intersection_point):
        intersection_bool = False

        int_line_x1 = intersection_line[0][0]
        int_line_x2 = intersection_line[1][0]
        int_line_y = intersection_line[0][1]

        int_pt_x, int_pt_y = intersection_point

        if int_line_x1 + 1 <= int_pt_x <= int_line_x2 - 1 and int_line_y-5 <= int_pt_y <= int_line_y + 5:
            intersection_bool = True
        else:
            intersection_bool = False

        return intersection_bool

    def check_real_intersection(self, intersection_point, intersection_line_coordinates):
        x, y = intersection_point
        pt1, pt2 = intersection_line_coordinates

        pt1_x, pt1_y = pt1
        pt2_x, pt2_y = pt2

        pt1_x += 1
        pt2_x -= 1

        if pt1_x <= x <= pt2_x and pt2_y - 5 < y < pt2_y + 5:
            real = True
        else:
            real = False

        return real

    def get_closest_line(self, line_coords, player_coords, ray_dir):

        player_x, player_y = player_coords

        line_points = []
        distances = []

        ordered_output = []

        unsorted_dict = {}

        for coords in line_coords:

            point_1, point_2 = coords

            point_1_x, point_1_y = point_1
            point_2_x, point_2_y = point_2
            avg_dist = 0

            if ray_dir[0] == 'U':
                if point_1_y < player_y:
                    #CONTINUE FINDING HOW FAR THE LINES ABOVE THE PLAYER ARE
                    d_x1 = math.sqrt((point_1_x - player_x) * (point_1_x - player_x))
                    d_y1 = math.sqrt((point_1_y - player_y) * (point_1_y - player_y))

                    d_x2 = math.sqrt((point_2_x - player_x) * (point_2_x - player_x))
                    d_y2 = math.sqrt((point_2_y - player_y) * (point_2_y - player_y))

                    abs_dist_1 = math.sqrt((d_x1 * d_x1) + (d_y1 * d_y1))
                    abs_dist_2 = math.sqrt((d_x2 * d_x2) + (d_y2 * d_y2))

                    avg_dist = (abs_dist_1 + abs_dist_2) / 2

                    unsorted_dict[avg_dist] = (point_1, point_2)

            if ray_dir[0] == 'D':
                if point_1_y > player_y:

                    d_x1 = math.sqrt((point_1_x - player_x) * (point_1_x - player_x))
                    d_y1 = math.sqrt((point_1_y - player_y) * (point_1_y - player_y))

                    d_x2 = math.sqrt((point_2_x - player_x) * (point_2_x - player_x))
                    d_y2 = math.sqrt((point_2_y - player_y) * (point_2_y - player_y))

                    abs_dist_1 = math.sqrt((d_x1*d_x1) + (d_y1*d_y1))
                    abs_dist_2 = math.sqrt((d_x2 * d_x2) + (d_y2 * d_y2))

                    avg_dist = (abs_dist_1 + abs_dist_2)/2

                    unsorted_dict[avg_dist] = (point_1, point_2)

        sorted_dict = collections.OrderedDict(sorted(unsorted_dict.items()))

        for coords in sorted_dict.values():
            ordered_output.append(coords)

        return ordered_output

    def update(self, player_coords, obstacle_coordinates):

        self.mouse_x, self.mouse_y = player_coords

        self.circle_coordinates = []
        self.ray_line_draw = []

        coords = [ (0, 0), (500, 0), (0, 500), (500, 500), (250, 500), (250, 0), (0, 250), (500, 250)]

        obst_coord = obstacle_coordinates

        for coord in coords:
            self.ray_list.append(self.ray(self.mouse_x, self.mouse_y, *coord))

            if len(self.ray_list) > len(coords):
                self.ray_list.pop(0)

        ray_number = 0

        ray_end_coords = []

        if len(self.ray_list) == len(coords):

            for coord in self.ray_list:
                ray_number += 1
                ray_start = coord[0]
                ray_end = coord[1]

                ray_end_point = ray_end

                start_line = self.line(ray_start, ray_end)

                pt_1 = (10, 10)
                pt_2 = (100, 100)

                intersections = 0

                ray_dir = self.find_line_dir(ray_start, ray_end)
                ordered_obstacles = self.get_closest_line(obst_coord, (self.mouse_x, self.mouse_y), ray_dir)

                for line_co in ordered_obstacles:

                    co_1, co_2 = line_co
                    int_line = self.line(co_1, co_2) #Intersection Line

                    if int_line != (0, 0, 0):
                        det_vals = self.intersection(start_line, int_line)

                        temp = self.generate_int_point(det_vals, (self.mouse_x, self.mouse_y), ray_end)
                        if temp != (0, 0):

                            self._x,self. _y = temp

                            int_point = (self._x, self._y)

                            self.line_intersection_bool = self.check_real_intersection(int_point, (co_1, co_2))

                            if self.line_intersection_bool:
                                ray_end_point = (self._x, self._y)
                                self.circle_coordinates.append(ray_end_point)
                                break

                            else:
                                ray_end_point = ray_end
                self.ray_line_draw.append((ray_start, ray_end_point))

    def draw(self):

        pygame.draw.circle(self.win, (255, 0, 0), (self.mouse_x, self.mouse_y), 3)

        if self.circle_coordinates:

            for coord in self.circle_coordinates:
                pygame.draw.circle(self.win, (255, 0, 0), (int(coord[0]), int(coord[1])), 3)

        if self.ray_line_draw:

            for coord in self.ray_line_draw:
                self.draw_ray(*coord)

