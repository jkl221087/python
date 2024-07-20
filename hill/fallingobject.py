# falling_object.py
# fallingobject.py

# falling_object.py

import pygame
import math
import random

class FallingObject:
    def __init__(self, width, height, size, color=(255, 0, 0)):
        self.width = width
        self.height = height
        self.size = size
        self.color = color
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, color, (0, 0, size, size))
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.width - self.size)
        self.y = -self.size
        self.velocity_x = 0
        self.velocity_y = 0
        self.rotation_angle = 0
        self.angular_velocity = 0
        self.gravity = 0.1
        self.stopped = False

    def update(self):
        if not self.stopped:
            # 計算物體與中心的水平距離
            center_x = self.width / 2
            direction_x = (center_x - (self.x + self.size / 2)) / center_x
            self.velocity_x += direction_x * 0.05  # 調整這個值以控制物體向中心移動的速度

            self.velocity_y += self.gravity
            self.x += self.velocity_x
            self.y += self.velocity_y

    def apply_physics(self, hill):
        if hill.is_on_hill(self.x, self.y, self.size):
            self.x, self.y = hill.adjust_position(self.x, self.y, self.size)
            hill_angle = hill.get_hill_angle(self.x + self.size / 2)

            parallel_velocity = self.velocity_x * math.cos(hill_angle) + self.velocity_y * math.sin(hill_angle)

            friction = 0.1
            parallel_velocity *= (1 - friction)

            self.velocity_x = parallel_velocity * math.cos(hill_angle)
            self.velocity_y = parallel_velocity * math.sin(hill_angle)

            self.angular_velocity = parallel_velocity / (self.size / 2)

            # Check if the object has stopped
            if abs(self.velocity_x) < 0.01 and abs(self.velocity_y) < 0.01:
                self.stopped = True

    def draw(self, screen):
        if self.stopped:
            self.reset()

        self.rotation_angle += math.degrees(self.angular_velocity)
        self.rotation_angle %= 360
        rotated_object, rotated_rect = self.rotate_center(self.surface, self.rotation_angle)
        rotated_rect.center = (int(self.x + self.size / 2), int(self.y + self.size / 2))
        screen.blit(rotated_object, rotated_rect)

    def rotate_center(self, image, angle):
        rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect
