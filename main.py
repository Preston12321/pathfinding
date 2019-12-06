import pygame
import level as lvl
import action_bar as ab
import astar2

COUNT_SPEED = 2

# Calculate the actual pixel dimensions of our window
WINDOW_WIDTH = lvl.CELL_WIDTH * lvl.CELL_COUNT_X + lvl.DIVIDER_WIDTH * (lvl.CELL_COUNT_X - 1)
WINDOW_HEIGHT = lvl.CELL_HEIGHT * lvl.CELL_COUNT_Y + lvl.DIVIDER_WIDTH * (lvl.CELL_COUNT_Y - 1) + ab.ACTION_BAR_HEIGHT


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialize the action bar
    action_bar = ab.ActionBar(WINDOW_WIDTH)

    # Initialize the default level
    level = lvl.Level()
    mouse_held = False
    button_clicked = None
    counter = 0
    run_clicked = False

    while True:
        # Handle events in the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button_clicked = action_bar.get_button_from_window(event.pos[0], event.pos[1])
                    if button_clicked is None:
                        mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False
                    button_under_mouse = action_bar.get_button_from_window(event.pos[0], event.pos[1])
                    if button_clicked is not None and button_clicked is button_under_mouse:
                        if button_clicked.text == "Run":
                            # Begin algorithm animation
                            run_clicked = True
                            counter = 0
                            level.clear_explored()
                            astar = astar2.a_star(level.start, level.destination)
                            path = astar[0]
                            cloud = astar[1]
                            # if path is not None:
                            #     for cell in path:
                            #         cell.set_explored(True)
                        if button_clicked.text == "Clear":
                            level.clear_walls()
                            level.set_neighbors()
                            counter = 0
                            cloud = []
                            path = []
                    button_clicked = None
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         cloud[counter].set_cloud(True)
            #         counter = counter + 1

        # animates cloud
        if counter % COUNT_SPEED == 0 and run_clicked and counter//COUNT_SPEED < len(cloud):
            cloud[counter//COUNT_SPEED].set_cloud(True)

        counter = counter + 1

        if run_clicked and counter//COUNT_SPEED >= len(cloud) and len(cloud) != 0:
            if path is not None:
                for cell in path:
                    cell.set_explored(True)

        # changes cells to wall when mouse is dragged over
        if mouse_held:
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
