import pygame
from pygame.locals import *
from consts import *
from asset_loader import *
from graph import Graph
from math import pi, sin, cos, tan, atan2, sqrt
from user import User
import time

"""
This file contains the main function for the exhibit
It initializes the Pygame window, loads assets, and runs the main loop.
It handles user input, updates the user position, and calculates the score based on the graph.
It also handles the drawing of the graph and the user points on the screen.
"""

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
    user = User(
                screen,
                (0, 1000), (-500, 500),
                (
                    asset_loader.pictures["grid"][1][0],
                    asset_loader.pictures["grid"][1][1],
                    asset_loader.pictures["grid"][0].get_width(),
                    asset_loader.pictures["grid"][0].get_height()
                ),
            )

    # Create a graph object
    graphs = [Graph(
                screen,
                lambda x: 300 * sin(0.02*x),
                (0, 1000), (-500, 500),
                (
                    asset_loader.pictures["grid"][1][0],
                    asset_loader.pictures["grid"][1][1],
                    asset_loader.pictures["grid"][0].get_width(),
                    asset_loader.pictures["grid"][0].get_height()
                )
            ),
            Graph(
                screen,
                lambda x: 0,
                (0, 1000), (-500, 500),
                (
                    asset_loader.pictures["grid"][1][0],
                    asset_loader.pictures["grid"][1][1],
                    asset_loader.pictures["grid"][0].get_width(),
                    asset_loader.pictures["grid"][0].get_height()
                )
            ),
            Graph(
                screen,
                lambda x: x - 500,
                (0, 1000), (-500, 500),
                (
                    asset_loader.pictures["grid"][1][0],
                    asset_loader.pictures["grid"][1][1],
                    asset_loader.pictures["grid"][0].get_width(),
                    asset_loader.pictures["grid"][0].get_height()
                )
            )]
    graph_index = 0

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    user.move_y(True)
                
                elif event.key == K_DOWN:
                    user.move_y(False)
            
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    user.move_y(True)
                else:
                    user.move_y(False)

        user.add_point()
        has_done_graph = user.move_x()

        if has_done_graph:
            graph_index = (graph_index + 1) % len(graphs)

        user.calc_score(graphs[graph_index])

        asset_loader.render(screen)
        
        # Draw the graph on the grid
        graphs[graph_index].draw()

        user.draw_graph()
        user.show_score()
        user.draw_user_lines()

        # time.sleep(TIME_DELAY)  # Delay to control the speed of the car

        pygame.display.flip()
        clock.tick(1000)


if __name__ == "__main__":
    main()