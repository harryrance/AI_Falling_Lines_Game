import pygame
import math
import collections

pygame.init()

win = pygame.display.set_mode((500, 500))
run = True

def ray(p_x, p_y, c_x, c_y):

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
    #print(rad_x)
    return (p_x, p_y), (end_x, end_y)

def draw_ray(pt_1, pt_2):
    pygame.draw.line(win, (255, 255, 255), pt_1, pt_2)

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])

    return A, B, -C

def det(L1, L2):
    return L1[0] * L2[1] - L1[1] * L2[0]

def find_line_dir(startpoint_coord, endpoint_coord):
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

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        return D, Dx, Dy
    else:
        return False

def generate_int_point(int_det, ray_start_coord, ray_end_coord):
    D, Dx, Dy = int_det

    line_1_dir = find_line_dir(ray_start_coord, ray_end_coord)
    line_2_dir = find_line_dir(ray_start_coord, (Dx / D, Dy / D))

    if line_1_dir == line_2_dir:
        x = Dx / D
        y = Dy / D

        return x, y
    else:
        return (0, 0)

def get_closest_intersection(intersection_line, intersection_point):
    intersection_bool = False

    int_line_x1 = intersection_line[0][0]
    int_line_x2 = intersection_line[1][0]
    int_line_y = intersection_line[0][1]

    int_pt_x, int_pt_y = intersection_point

    if int_line_x1 + 1 <= int_pt_x <= int_line_x2 - 1 and int_line_y-10 <= int_pt_y <= int_line_y + 10:
        intersection_bool = True
    else:
        intersection_bool = False

    return intersection_bool

def check_real_intersection(intersection_point, intersection_line_coordinates):
    x, y = intersection_point
    pt1, pt2 = intersection_line_coordinates

    pt1_x, pt1_y = pt1
    pt2_x, pt2_y = pt2

    pt1_x += 1
    pt2_x -= 1

    if pt1_x <= x <= pt2_x and pt2_y - 10 < y < pt2_y + 10:
        real = True
    else:
        real = False

    return real

def get_closest_line(line_coords, player_coords, ray_dir):

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

ray_list = []

while run:
    pygame.time.delay(5)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    win.fill((0, 0, 0))

    coords = [ (0, 0), (500, 0), (0, 500), (500, 500), (0, 300), (150, 300), (0, 400), (50, 400), (150, 400), (500, 400), (250, 300), (500, 300)]
    obst_coord = [((0, 300), (150, 300)), ((0, 400), (50, 400)), ((150, 400), (500, 400)), ((250, 300), (500, 300))]

    for coord in coords:
        ray_list.append(ray(mouse_x, mouse_y, *coord))

        if len(ray_list) > len(coords):
            ray_list.pop(0)

    obst_1 = pygame.draw.line(win, (0, 150, 100), (0, 300), (150, 300), 2)
    obst_2 = pygame.draw.line(win, (0, 150, 100), (250, 300), (500, 300), 2)
    obst_3 = pygame.draw.line(win, (0, 150, 100), (0, 400), (50, 400), 2)
    obst_4 = pygame.draw.line(win, (0, 150, 100), (150, 400), (500, 400), 2)

    ray_number = 0

    ray_end_coords = []
    if len(ray_list) == len(coords):
        for coord in ray_list:
            ray_number += 1
            ray_start = coord[0]
            ray_end = coord[1]

            ray_end_point = ray_end

            start_line = line(ray_start, ray_end)

            pt_1 = (10, 10)
            pt_2 = (100, 100)

            intersections = 0

            ray_dir = find_line_dir(ray_start, ray_end)
            ordered_obstacles = get_closest_line(obst_coord, (mouse_x, mouse_y), ray_dir)

            #for line_co in obst_coord:
            for line_co in ordered_obstacles:

                co_1, co_2 = line_co
                int_line = line(co_1, co_2) #Intersection Line

                det_vals = intersection(start_line, int_line)

                temp = generate_int_point(det_vals, (mouse_x, mouse_y), ray_end)
                if temp != (0, 0):
                    _x, _y = temp

                    int_point = (_x, _y)

                    line_intersection_bool = check_real_intersection(int_point, (co_1, co_2))

                    if line_intersection_bool:
                        pygame.draw.circle(win, (255, 0, 0), (int(_x), int(_y)), 3)
                        ray_end_point = (_x, _y)

                        break

                    else:
                        ray_end_point = ray_end

            draw_ray(ray_start, ray_end_point)

    # Draw Obstacle

    pygame.draw.circle(win, (255, 0, 0), (mouse_x, mouse_y), 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()