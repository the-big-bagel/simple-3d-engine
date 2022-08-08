import pygame
import math

pygame.init()
screen = pygame.display.set_mode((2000,1300))
pygame.display.set_caption("3D Engine")

cube = [[0, 200, 0], [0, 250, 0], [50, 250, 0], [50, 200, 0], [50, 250, 50], [50, 200, 50], [0, 250, 50], [0, 200, 50]]
square_pos = [0, -200, 0]
camera_pos = [0, 0, 0]
camera_angle = [00, 0]
clock = pygame.time.Clock()
esc = False
render_list = []

def get_angle_flat(p):
    a = 69
    if p[0] > 0:
        if p[1] > 0:
            quad = 1
        elif p[1] < 0:
            quad = 4
        else:
            a = 0
            
    elif p[0] < 0:
        if p[1] > 0:
            quad = 2
        elif p[1] < 0:
            quad = 3
        else:
            a = math.pi
    else:
        if p[1] > 0:
            a = math.pi/2
        elif p[1] < 0:
            a = -math.pi/2
        else:
            a = "null"
    
    if a != 0 and a != math.pi and a != math.pi/2 and a != -math.pi/2:
        if quad == 1:
            a = math.atan(p[1]/p[0])
        elif quad == 2:
            a = math.pi+math.atan(p[1]/p[0])
        elif quad == 3:
            a = -(math.pi-math.atan(p[1]/p[0]))
        elif quad == 4:
            a = math.atan(p[1]/p[0])
    return a

def get_angle_side(p):
    a = 2
    if p[1] > 0:
        if p[2] > 0:
            quad = 1
        elif p[2] < 0:
            quad = 4
        else:
            a = 0
            
    elif p[1] < 0:
        if p[2] > 0:
            quad = 2
        elif p[2] < 0:
            quad = 3
        else:
            a = math.pi
    else:
        if p[2] > 0:
            a = math.pi/2
        elif p[2] < 0:
            a = -math.pi/2
        else:
            a = "null"
    
    if a != 0 and a != math.pi and a != math.pi/2 and a != -math.pi/2:
        if quad == 1:
            a = math.atan(p[2]/p[1])
        elif quad == 2:
            a = math.pi+math.atan(p[2]/p[1])
        elif quad == 3:
            a = -(math.pi-math.atan(p[2]/p[1]))
        elif quad == 4:
            a = math.atan(p[2]/p[1])
    return a


def to_degrees(a):
    return a*180/math.pi

def distance(p):
    dis = math.sqrt(pow(p[0], 2) + pow(p[1], 2))
    return dis

def distance_2(p):
    dis = math.sqrt(pow(p[1], 2) + pow(p[2], 2))
    return dis

def to_radians(a):
    return a/180*math.pi

while True:
    render_list = []
    if not esc:
        pygame.mouse.set_pos((1000, 650))
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_w]:
        for item in cube:
            item[1] -= 1
    if pressed[pygame.K_a]:
        for item in cube:
            item[0] += 1
    if pressed[pygame.K_s]:
        for item in cube:
            item[1] += 1
    if pressed[pygame.K_d]:
        for item in cube:
            item[0] -= 1
    if pressed[pygame.K_SPACE]:
        for item in cube:
            item[2] += 1
    if pressed[pygame.K_LSHIFT]:
        for item in cube:
            item[2] -= 1

    if pressed[pygame.K_ESCAPE]:
        esc = not esc
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = list(mouse_pos)
    mouse_pos[0] = 1000 - mouse_pos[0]
    mouse_pos[1] = 650 - mouse_pos[1]

    print(math.cos(to_radians(camera_angle[0])))

    past_c_a = camera_angle.copy()
    if not esc:
        camera_angle[0] += mouse_pos[0]/3
        camera_angle[1] -= mouse_pos[1]/3

    if camera_angle[0] > 360:
        camera_angle[0] = 0
    elif camera_angle[0] < 0:
        camera_angle[0] = 360
    if camera_angle[1] > 360:
        camera_angle[1] = 0
    elif camera_angle[1] < 0:
        camera_angle[1] = 360
    if camera_angle != past_c_a:
        for i in range(len(cube)):
            dist = distance(cube[i])
            cube[i] = [math.cos(to_radians(to_degrees(get_angle_flat(cube[i])) + (past_c_a[0]-camera_angle[0])))*dist, math.sin(to_radians(to_degrees(get_angle_flat(cube[i])) + (past_c_a[0]-camera_angle[0])))*dist, cube[i][-1]]
            dist2 = distance_2(cube[i])
            cube[i] = [cube[i][0], math.cos(to_radians(to_degrees(get_angle_side(cube[i])) + (past_c_a[1]-camera_angle[1])))*dist2, math.sin(to_radians(to_degrees(get_angle_side(cube[i])) + (past_c_a[1]-camera_angle[1])))*dist2]

    for i in range(len(cube)):
        if cube[i][1] > 0:
            size = [cube[i][1]*5/2, cube[i][1]*3.25/2]
            render_list.append([cube[i][0]*(2000/size[0])+1000, cube[i][2]*(1300/size[1])+650])
        else:
            render_list.append("null")

    if "null" not in render_list:
        pygame.draw.line(screen, (255, 255, 255), render_list[0], render_list[1], 2)
        pygame.draw.line(screen, (255, 255, 255), render_list[0], render_list[3], 2)
        pygame.draw.line(screen, (255, 255, 255), render_list[0], render_list[-1], 2)

        pygame.draw.line(screen, (255, 255, 255), render_list[1], render_list[-2], 2)
        pygame.draw.line(screen, (255, 255, 255), render_list[1], render_list[2], 2)

        pygame.draw.line(screen, (255, 255, 255), render_list[2], render_list[4], 2)

        pygame.draw.line(screen, (255, 255, 255), render_list[3], render_list[-3], 2)

        pygame.draw.line(screen, (255, 255, 255), render_list[4], render_list[-2], 2)
        pygame.draw.line(screen, (255, 255, 255), render_list[4], render_list[-3], 2)

        pygame.draw.line(screen, (255, 255, 255), render_list[7], render_list[-2], 2)
        pygame.draw.line(screen, (255, 255, 255), render_list[7], render_list[-3], 2)

        pygame.draw.line(screen, (255, 255, 255), render_list[3], render_list[2], 2)

    pygame.display.update()
    clock.tick(120)
