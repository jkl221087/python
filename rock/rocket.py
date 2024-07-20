import random

import pygame
import math


class Rocket:
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.size = size
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.surface, (255, 0, 0), [(0, size), (size // 2, 0), (size, size)])
        self.reset()

        # 初始化字型
        self.font = pygame.font.SysFont(None, 24)

    def reset(self):
        self.x = self.width // 2
        self.y = self.height - self.size
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 9.81  # 重力加速度 (m/s^2)
        self.thrust = 1000.0  # 推力 (N)
        self.air_resistance = 0.47  # 空氣阻力係數
        self.cross_sectional_area = 0.1  # 火箭的橫截面積 (m^2)
        self.mass = 500.0  # 火箭質量 (kg)
        self.angle = 0
        self.angular_velocity = 0
        self.thrust_angle = 0
        self.stopped = False
        self.fuel = 60 # 初始燃料量 (kg)
        self.burn_rate = 10.0  # 燃料消耗率 (kg/s)
        self.wind_speed = random.uniform(0, 500)
        self.wind_direction = random.uniform(0, 360)

    def update(self, dt):
        if not self.stopped:

            self.wind_speed = random.uniform(0, 500)
            self.wind_direction = random.uniform(0, 360)
            # 計算推力分量
            thrust_x = self.thrust * math.sin(math.radians(self.thrust_angle))
            thrust_y = self.thrust * math.cos(math.radians(self.thrust_angle))

            # 計算速度
            speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)

            # 計算空氣阻力
            drag = 0.5 * self.air_resistance * self.cross_sectional_area * 1.225 * speed ** 2  # 空氣密度 (kg/m^3)
            drag_x = -drag * (self.velocity_x / max(speed, 1e-6))  # 避免除以零
            drag_y = -drag * (self.velocity_y / max(speed, 1e-6))  # 避免除以零

            wind_x = self.wind_speed * math.cos(math.radians(self.wind_direction))
            wind_y = self.wind_speed * math.sin(math.radians(self.wind_direction))

            # 計算加速度
            ax = (thrust_x + drag_x + wind_x) / max(self.mass, 1e-6)  # 避免除以零
            ay = (thrust_y + drag_y - self.gravity * self.mass + wind_y) / max(self.mass, 1e-6)  # 避免除以零

            # 更新速度和位置
            self.velocity_x += ax * dt
            self.velocity_y += ay * dt
            self.x += self.velocity_x * dt
            self.y -= self.velocity_y * dt

            # 更新燃料和質量
            fuel_consumed = self.burn_rate * dt
            self.fuel = max(0, self.fuel - fuel_consumed)
            if self.fuel <= 0:
                self.fuel = 0
                self.thrust = 0  # 停止推力

            self.mass = max(100, self.mass - fuel_consumed)  # 確保質量不會低於最小值

            # 更新角度
            self.angle += self.angular_velocity * dt
            self.angle %= 360

            # 檢查是否著陸或飛出屏幕
            if self.y >= self.height - self.size:
                self.y = self.height - self.size
                self.velocity_y = 0
                self.stopped = False
            elif self.y < 0 or self.x < 0 or self.x > self.width:
                self.stopped = False

    def apply_thrust(self, thrust):
        if not self.stopped:
            self.thrust = thrust
        print(self.thrust)

    def draw(self, screen):
        # 旋轉火箭表面
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.size / 2, self.y + self.size / 2))
        screen.blit(rotated_surface, rotated_rect)

        # 顯示狀態資訊
        font = pygame.font.Font('NotoSansTC-Regular.ttf', 24)
        info = [
            f"燃料: {self.fuel:.2f} kg",
            f"速度 X: {self.velocity_x:.2f} m/s",
            f"速度 Y: {self.velocity_y:.2f} m/s",
            f"空氣阻力: {self.air_resistance:.2f}",
            f"推力: {self.thrust:.2f} N",
            f"質量: {self.mass:.2f} kg",
            f"風速: {self.wind_speed:.2f} m/s",
            f"風向: {self.wind_direction:.2f} °"
        ]

        y_offset = 10
        for line in info:
            text_surface = font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (10, y_offset))
            y_offset += 25
