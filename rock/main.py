import pygame
from rocket import Rocket


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
        if keys[pygame.K_DOWN]:
            rocket.apply_thrust(10000.0)
        elif rocket.fuel == 0:
            rocket.apply_thrust(0.0)
        else:
            rocket.apply_thrust(11000.0)

        # 更新火箭狀態
        rocket.update(dt)

        # 更新畫面
        screen.fill((255, 255, 255))
        rocket.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

