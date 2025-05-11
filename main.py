import pygame
from pygame.locals import *
from consts import *
from assetLoader import *
from graph import Graph
from math import pi, sin, cos, tan, atan2, sqrt

def main():
    
    pygame.init()
    pygame.display.set_caption("Car Plot")
    clock = pygame.time.Clock()
    
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        view_port = (screen_width, screen_height)

    else:
        screen = pygame.display.set_mode(VIEWPORT)
        view_port = VIEWPORT
    
    asset_loader = AssetLoader(ASSETS_DIR, PICTURES_TO_LOAD, view_port) 

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        
        asset_loader.render(screen)

        # Create a graph object
        graph = Graph(lambda x: 100 * sin(x))
        # Draw the graph on the grid
        graph.draw(screen, (-2*pi, 2*pi), (-200, 200), (asset_loader.pictures["grid"][1][0],
                                                    asset_loader.pictures["grid"][1][1],
                                                    asset_loader.pictures["grid"][0].get_width(),
                                                    asset_loader.pictures["grid"][0].get_height()),
                                                    step=0.1)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()