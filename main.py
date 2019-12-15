import pygame
import level as lvl
import action_bar as ab
import a_star

COUNT_SPEED = 2

# Calculate the pixel dimensions of our window
WINDOW_WIDTH = lvl.CELL_WIDTH * lvl.CELL_COUNT_X + lvl.DIVIDER_WIDTH * (lvl.CELL_COUNT_X - 1)
WINDOW_HEIGHT = lvl.CELL_HEIGHT * lvl.CELL_COUNT_Y + lvl.DIVIDER_WIDTH * (lvl.CELL_COUNT_Y - 1) + ab.ACTION_BAR_HEIGHT


def main():
    # Initialize Pygame and get a reference to the window's surface object
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialize the action bar
    action_bar = ab.ActionBar(WINDOW_WIDTH)

    # Initialize the level
    level = lvl.Level()

    # Loop status variables
    mouse_held = False
    button_clicked = None
    counter = 0
    run_clicked = False
    drawing_cloud = True

    # Main game loop; runs until user exits the program
    while True:
        # Handle events in the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click
                if event.button == 1:
                    # Get button at given coordinates in the window
                    button_clicked = action_bar.get_button_from_window(event.pos[0], event.pos[1])
                    if button_clicked is None:
                        mouse_held = True

            if event.type == pygame.MOUSEBUTTONUP:
                # Left click
                if event.button == 1:
                    mouse_held = False
                    # Get button at given coordinates in the window
                    button_under_mouse = action_bar.get_button_from_window(event.pos[0], event.pos[1])
                    if button_clicked is not None and button_clicked is button_under_mouse:
                        if button_clicked.text == "Run":
                            # Begin algorithm animation
                            run_clicked = True
                            counter = 0

                            # Clear decorations from cells
                            level.clear_explored()

                            # Call A* to get the best path and the cloud of explored nodes
                            path, cloud = a_star.a_star(level.start, level.destination)

                        if button_clicked.text == "Clear":
                            # Clear all cell decorations and walls
                            level.clear_walls()

                            # Re-link any cells that were walls to their neighbors
                            level.set_neighbors()

                            # Reset algorithm animation state
                            counter = 0
                            cloud = []
                            path = []

                    button_clicked = None

        # Animate cloud after every COUNT_SPEED'th frame
        if run_clicked:
            if counter % COUNT_SPEED == 0 and run_clicked:
                if drawing_cloud:
                    if counter//COUNT_SPEED < len(cloud):
                        cloud[counter//COUNT_SPEED].set_cloud(True)

                    if counter//COUNT_SPEED == len(cloud):
                        if path is None:
                            run_clicked = False
                        else:
                            counter = 0
                            drawing_cloud = False

                if not drawing_cloud:
                    if counter//COUNT_SPEED < len(path):
                        path[counter//COUNT_SPEED].set_explored(True)

                    if counter//COUNT_SPEED == len(path):
                        drawing_cloud = True
                        run_clicked = False

            counter = counter + 1

        # Change cells to walls when mouse is dragged over
        if mouse_held and not run_clicked:
            mouse_pos = pygame.mouse.get_pos()
            mouse_cell = level.get_cell_from_window(mouse_pos[0], mouse_pos[1])
            level.set_wall(mouse_cell)

        # Render frame to screen
        updates = level.render(window)
        updates.extend(action_bar.render(window))
        pygame.display.update(updates)

        # Wait between frames
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
