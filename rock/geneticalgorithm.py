import pygame
import math
import random

class Rocket:
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.size = size
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.surface, (255, 0, 0), [(0, size), (size // 2, 0), (size, size)])
        self.reset()

    def reset(self):
        self.x = self.width // 2  # 火箭初始 x 坐標
        self.y = self.height - self.size  # 火箭初始 y 坐標
        self.velocity_x = 0  # 初始 x 方向速度
        self.velocity_y = 0  # 初始 y 方向速度
        self.gravity = 9.81  # 重力加速度 (m/s^2)
        self.thrust = 0.0  # 初始推力 (N)
        self.air_resistance = 0.47  # 空氣阻力係數
        self.cross_sectional_area = 0.1  # 火箭的橫截面積 (m^2)
        self.mass = 500.0  # 火箭質量 (kg)
        self.angle = 0  # 火箭角度
        self.angular_velocity = 0  # 角速度
        self.thrust_angle = 0  # 推力角度
        self.stopped = False  # 是否停止
        self.fuel = 10000  # 初始燃料量 (kg)
        self.burn_rate = 10.0  # 燃料消耗率 (kg/s)
        self.in_air = False  # 火箭是否在空中
        self.max_height = 0  # 最大高度
        self.trajectory = []  # 軌跡
        self.is_landing = False  # 是否在降落
        self.landing_thrust = 500.0  # 降落時的推力 (N)
        self.wind_speed = random.uniform(0, 10)  # 初始風速 (m/s)
        self.wind_direction = random.uniform(0, 360)  # 初始風的方向 (角度，0 表示右，90 表示上)

    def update(self, dt):
        if self.fuel <= 0:
            self.thrust = 0  # 燃料耗盡時停止推力

        if not self.stopped:
            # 動態更新風速和風向
            self.wind_speed = random.uniform(0, 10)
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

            # 計算風對火箭的影響
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
                self.thrust = 0  # 燃料耗盡時停止推力

            self.mass = max(100, self.mass - fuel_consumed)  # 確保質量不低於最小值

            # 更新角度
            self.angle += self.angular_velocity * dt
            self.angle %= 360

            # 檢查是否達到最高點
            if self.y <= 0:
                self.y = 0
                self.velocity_y = 0
                self.in_air = False
                self.is_landing = True  # 開始降落

            if not self.in_air:
                if self.is_landing:
                    # 降落過程中施加推力以減慢下落速度
                    self.thrust = self.landing_thrust
                    if self.y >= self.height - self.size:
                        self.y = self.height - self.size
                        self.velocity_y = 0
                        self.stopped = True
                        self.in_air = False
                else:
                    # 重置位置以進行新一輪飛行
                    self.y = self.height - self.size
                    self.x = self.width // 2
                    self.velocity_x = 0
                    self.velocity_y = 0
                    self.stopped = True
                    self.in_air = True

            # 記錄最大高度
            self.max_height = max(self.max_height, self.height - self.y)
            self.trajectory.append((self.x, self.y))

    def apply_thrust(self, thrust):
        if not self.stopped:
            self.thrust = thrust

    def draw(self, screen):
        # 旋轉火箭表面
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x + self.size / 2, self.y + self.size / 2))
        screen.blit(rotated_surface, rotated_rect)

        # 使用支持 UTF-8 字符的字體
        font = pygame.font.Font('NotoSansCJK-Regular.ttc', 24)
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

        # 繪製軌跡
        if len(self.trajectory) > 1:
            pygame.draw.lines(screen, (0, 0, 255), False, self.trajectory, 1)


def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Rocket Simulation')

    rocket_size = 50
    rocket = Rocket(width, height, rocket_size)

    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60) / 1000.0  # 獲取時間間隔（秒）

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            rocket.apply_thrust(45)
        else:
            rocket.apply_thrust(0)

        # 更新火箭狀態
        rocket.update(dt)

        # 更新畫面
        screen.fill((255, 255, 255))
        rocket.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
