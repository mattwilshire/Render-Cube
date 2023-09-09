import pygame
import numpy as np
from math import *

mouse_pos = [-1, -1]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 155)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("Cube Render")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100

circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

angle = 0
camera_x = 1
camera_y = 1
camera_dist = 1

points = []

# all the cube vertices
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))
print(np.matrix([-1, -1, 1]).reshape(3, 1))


projected_points = [
    [n, n] for n in range(len(points))
]

def render():
    rotation_z = np.matrix([
        [cos(angleZ), -sin(angleZ), 0],
        [sin(angleZ), cos(angleZ), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angleY), 0, sin(angleY)],
        [0, 1, 0],
        [-sin(angleY), 0, cos(angleY)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angleX), -sin(angleX)],
        [0, sin(angleX), cos(angleX)],
    ])

    screen.fill(BLACK)

    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        distance = 2
        z = 1 / ( (distance * camera_dist)  - rotated2d[2].item())

        projection_matrix = np.matrix([
            [z, 0, 0],
            [0, z, 0]
        ])

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x + camera_x, y + camera_y]
        pygame.draw.circle(screen, BLACK, (x + camera_x, y + camera_y), 2)
        i += 1

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)


def connect_points(i, j, points):
    pygame.draw.line(
        screen, GREEN, (points[i][0], points[i][1]), (points[j][0], points[j][1]), 2)


clock = pygame.time.Clock()
angleZ = 0
angleX = 0
angleY = 0
while True:

    clock.tick(230)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_dist -= 0.1
    elif keys[pygame.K_s]:
        camera_dist += 0.1
    elif keys[pygame.K_a]:
        camera_x += 5
    elif keys[pygame.K_d]:
        camera_x -= 5
    elif keys[pygame.K_LEFT]:
        angleY -= 0.1
    elif keys[pygame.K_RIGHT]:
        angleY += 0.1
    elif keys[pygame.K_UP]:
        angleX += 0.1
    elif keys[pygame.K_DOWN]:
        angleX -= 0.1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                camera_dist -= 0.1
            elif event.key == pygame.K_s:
                camera_dist += 0.1
            elif event.key == pygame.K_a:
                camera_x += 5
            elif event.key == pygame.K_d:
                camera_x -= 5
            elif event.key == pygame.K_LEFT:
                angleY -= 0.3
            elif event.key == pygame.K_RIGHT:
                angleY += 0.3
            elif event.key == pygame.K_UP:
                angleX += 0.3
            elif event.key == pygame.K_DOWN:
                angleX -= 0.3

        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
            if mouse_pos == [-1, -1]:
                mouse_pos = [mouse_position[0], mouse_position[1]]
            else:
                translate = np.subtract(mouse_pos, mouse_position)
                mouse_pos = [mouse_position[0], mouse_position[1]]
                # TODO: mouse_pos[0] * sens
    render()

    pygame.display.update()