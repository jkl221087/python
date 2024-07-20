# main.py

# main.py

import pygame
from hill import Hill
from fallingobject import FallingObject

def main():
    pygame.init()
    width, height = 300, 500
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Falling Box on Hill')

    hill_height = height // 7
    hill = Hill(width, height, hill_height)

    object_size = 50
    falling_object = FallingObject(width, height, object_size)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        falling_object.update()
        falling_object.apply_physics(hill)

        screen.fill((255, 255, 255))
        pygame.draw.polygon(screen, (34, 139, 34),
                            [(x, hill.get_hill_y(x)) for x in range(width)] +
                            [(width, height), (0, height)])
        falling_object.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
