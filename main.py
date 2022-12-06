import pygame
import heapq
from pygame.locals import *
from drop_down_menu import UIDropDownMenu
from searching_algo import *

# Initialize
FPS = 60
pygame.init()
WIDTH = 600
HEIGHT = 600
pygame.display.set_caption("Puzzel beta version on the beta")
window = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
SIZE_R = WIDTH // ROW
SIZE_C = HEIGHT // COL
steps = []
selected_button = None
hold_wall_draw = False
found_exit = [False]
puzzel_field = create_matrix()
way_to_unlock = {}
font = pygame.font.SysFont("Arial", 16)
drop_down_menu = UIDropDownMenu(391, 0, 150, 20, font,
                                ["Select Algorithm", "Recurse", "BFS", "DFS", "Dijkstra's", "NNS"])
open_menu = False


def re_scale_all_pictures():
    for key, link in PICTURES.items():
        if key == "square_start_point":
            menu["start flag"] = pygame.transform.scale(pygame.image.load(link), (SIZE_C * 2, SIZE_R * 2))
        elif key == "square_end_point":
            menu["end flag"] = pygame.transform.scale(pygame.image.load(link), (SIZE_C * 2, SIZE_R * 2))
        elif key == "square_wall":
            menu["wall"] = pygame.transform.scale(pygame.image.load(link), (SIZE_C * 2, SIZE_R * 2))
        elif key == "square_start":
            menu["start"] = pygame.transform.scale(pygame.image.load(link), (SIZE_C * 2, SIZE_R * 2))
        PICTURES[key] = pygame.transform.scale(pygame.image.load(link), (SIZE_C, SIZE_R))


def game_over_result():
    for row in range(START_ROW, ROW):
        for col in range(COL):
            puzzel_field[row][col].show_square()


def recurse_search_for_exit(row, col):
    if not check_valid_position(row, col) or found_exit[0]:
        return
    steps.append((row, col))
    if puzzel_field[row][col] == matrix_pos["exit coordinates"]:
        found_exit[0] = True
        way_to_unlock[len(steps)] = steps.copy()
        return
    matrix_field_where_steps(row, col)
    [recurse_search_for_exit(row, col) for row, col in ((row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col))]
    steps.remove((row, col))


def matrix_field_where_steps(row, col):
    puzzel_field[row][col].check_col(puzzel_field[row][col])
    puzzel_field[row][col].visited = "Yes"
    puzzel_field[row][col].open_field = True
    draw_square()
    pygame.display.update()
    pygame.time.wait(20)


def print_shortest_path(coordinates: list):
    try:
        for row, col in coordinates[1:-1]:
            puzzel_field[row][col].picture = "square_f"
            draw_square()
            pygame.display.update()
            pygame.time.wait(20)
    except TypeError:
        pass


def check_valid_position(row, col):
    if not check_valid_index(row, col) or puzzel_field[row][col].visited == "Yes" \
            or puzzel_field[row][col].wall_square or row == 1 or row == 0:
        return False
    return True


def bfs_search_for_exit(row, col):
    # Define a function to find the shortest path using BFS
    def find_shortest_path(start=(row, col), end=matrix_pos["exit coordinates"].position):
        # Initialize a queue with the starting position
        queue = [(start, [start])]
        visited = set()

        # Loop until the queue is empty
        while queue:
            # Get the next position and its path
            pos, path = queue.pop(0)

            # Check if the position is the end
            if pos == end:
                return path

            # Check all possible moves from the current position
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if check_valid_position(*new_pos) and new_pos not in visited:
                    queue.append((new_pos, path + [new_pos]))
                    matrix_field_where_steps(*new_pos)
                    visited.add(new_pos)

        # Return an empty path if the end cannot be reached
        return []

    # Find the shortest path between two points
    shortest_path = find_shortest_path()

    # Print the result
    print_shortest_path(shortest_path)


def dfs_search_for_exit(row, col):
    # Define a function to find the shortest path using the DFS algorithm
    def find_shortest_path(start, end, path):
        # Check if the start position is the end
        if start == end:
            return path

        # Check all possible moves from the current position
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (start[0] + direction[0], start[1] + direction[1])
            if check_valid_position(*new_pos) and new_pos not in visited:
                visited.add(new_pos)
                matrix_field_where_steps(*new_pos)
                new_path = find_shortest_path(new_pos, end, path + [new_pos])

                if new_path:
                    return new_path

        # Return None if the end cannot be reached
        return None

    start = (row, col)
    end = matrix_pos["exit coordinates"].position
    visited = set()
    visited.add(start)
    shortest_path = find_shortest_path(start, end, [start])

    # Print the result
    print_shortest_path(shortest_path)


def dijkstra_search_for_exit(row, col):
    # Define a function to find the shortest path using Dijkstra's algorithm
    def find_shortest_path(start=(row, col), end=matrix_pos["exit coordinates"].position):
        # Create a priority queue of distances and paths
        queue = []
        heapq.heappush(queue, (0, [start]))

        # Create a set to keep track of visited positions
        visited = set()

        # Loop until the queue is empty
        while queue:
            # Get the next distance and path from the queue
            dist, path = heapq.heappop(queue)

            # Get the last position in the path
            pos = path[-1]

            # Check if the position is the end
            if pos == end:
                return path

            # Check if the position has been visited
            if pos in visited:
                continue

            # Mark the position as visited
            visited.add(pos)

            # Check all possible moves from the current position
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if check_valid_position(*new_pos):
                    new_dist = dist + 1  # Update the distance
                    new_path = path + [new_pos]  # Update the path
                    heapq.heappush(queue, (new_dist, new_path))
                    matrix_field_where_steps(*new_pos)

    print_shortest_path(find_shortest_path())


def nns_search_for_exit(row, col):
    # Define a function to find the shortest path using nearest neighbor search
    def find_shortest_path(start=(row, col), end=matrix_pos["exit coordinates"].position):
        # Create a list of paths
        paths = [[start]]

        # Create a set to keep track of visited positions
        visited = set()

        # Loop until the list of paths is empty
        while paths:
            # Get the next path from the list
            path = paths.pop(0)

            # Get the last position in the path
            pos = path[-1]

            # Check if the position is the end
            if pos == end:
                return path

            # Check if the position has been visited
            if pos in visited:
                continue

            # Mark the position as visited
            visited.add(pos)

            # Check all possible moves from the current position
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if check_valid_position(*new_pos):
                    new_path = path + [new_pos]  # Update the path
                    paths.append(new_path)
                    matrix_field_where_steps(*new_pos)
        return path

    print_shortest_path(find_shortest_path())


def selected_menu(selected_button, pos):
    rect = menu[selected_button].get_rect(center=(pos * SIZE_C, SIZE_R))
    pygame.draw.rect(window, "BLUE", rect, 4)


def draw_menu():
    [window.blit(menu[x], (y * SIZE_C, 0 * SIZE_R)) for x, y in
     (("start flag", 0), ("end flag", 3), ("wall", 6), ("start", 9))]


def draw_square():
    for row in range(ROW):
        for col in range(COL):
            window.blit(PICTURES[puzzel_field[row][col].picture], (col * SIZE_C, row * SIZE_R))
    drop_down_menu.draw(window)
    draw_menu()
    if selected_button:
        selected_menu(*selected_button)


re_scale_all_pictures()

algorithm = {
    1: recurse_search_for_exit,
    2: bfs_search_for_exit,
    3: dfs_search_for_exit,
    4: dijkstra_search_for_exit,
    5: nns_search_for_exit
}

while running:
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        try:
            col, row = [x // size for x, size in zip(pygame.mouse.get_pos(), (SIZE_C, SIZE_R))]
            symbol = puzzel_field[row][col]
        except IndexError:
            continue

        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hold_wall_draw = True
            left_click, _, right_click = pygame.mouse.get_pressed()
            print(row, col)
            drop_down_menu.handle_events(event)
            if row in (0, 1):
                if col in (0, 1):
                    selected_button = ("start flag", 1)
                    if menu["selected"]["start"]:
                        matrix_pos["start coordinates"].picture = "square_empty"
                        matrix_pos["start coordinates"] = symbol

                    menu["selected"]["end"] = False
                    menu["selected"]["wall"] = False
                    menu["selected"]["start"] = True

                elif col in (3, 4):
                    selected_button = ("end flag", 4)
                    if menu["selected"]["end"]:
                        matrix_pos["exit coordinates"].picture = "square_empty"
                        matrix_pos["exit coordinates"] = symbol

                    menu["selected"]["start"] = False
                    menu["selected"]["wall"] = False
                    menu["selected"]["end"] = True

                elif col in (6, 7):
                    menu["selected"]["wall"] = True
                    selected_button = ("wall", 7)
                    menu["selected"]["start"] = False
                    menu["selected"]["end"] = False

                elif col in (9, 10):
                    selected_button = ("start", 10)
                    menu["selected"]["start"] = False
                    menu["selected"]["end"] = False
                    menu["selected"]["wall"] = False
                    if all(x for x in matrix_pos.values()) and drop_down_menu.selected_index != 0:
                        menu["selected"]["go"] = True
                        algorithm[drop_down_menu.selected_index](*matrix_pos["start coordinates"].position)

            elif open_menu:
                continue

            elif left_click and menu["selected"]["go"]:
                menu["selected"]["go"] = False
                puzzel_field = create_matrix()

            elif left_click and menu["selected"]["start"]:
                symbol.position_add(symbol, "start coordinates", "square_start_point")

            elif left_click and menu["selected"]["end"]:
                symbol.position_add(symbol, "exit coordinates", "square_end_point")

            elif left_click and menu["selected"]["wall"] and symbol.picture not in (
                    "square_end_point", "square_start_point"):
                symbol.wall(False)

        if event.type == pygame.MOUSEBUTTONUP:
            hold_wall_draw = False

        elif hold_wall_draw and menu["selected"][
            "wall"] and event.type == MOUSEMOTION and symbol.name != "BLANK" and not open_menu and symbol.picture not in (
                "square_end_point", "square_start_point"):
            symbol.wall(True)

    draw_square()
    pygame.display.update()
    open_menu = drop_down_menu.is_open
pygame.quit()
