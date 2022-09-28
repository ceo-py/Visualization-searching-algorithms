import pygame
from pygame.locals import *
from searching_algo import *

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
puzzel_field = create_matrix()
way_to_unlock = {}


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


def search_for_exit(row, col):
    if not check_valid_index(row, col) or puzzel_field[row][col].visited == "Yes" \
            or puzzel_field[row][col].wall_square or row == 1 or row == 0:
        return
    steps.append((row, col))
    if puzzel_field[row][col] == matrix_pos["exit coordinates"]:
        way_to_unlock[len(steps)] = steps.copy()
        return
    puzzel_field[row][col].check_col(puzzel_field[row][col])
    puzzel_field[row][col].visited = "Yes"
    puzzel_field[row][col].open_field = True
    draw_square()
    pygame.display.update()
    pygame.time.wait(20)
    [search_for_exit(row, col) for row, col in ((row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col))]
    steps.remove((row, col))


def selected_menu(selected_button, pos):
    rect = menu[selected_button].get_rect(center=(pos * SIZE_C, SIZE_R))
    pygame.draw.rect(window, "BLUE", rect, 4)


def draw_menu():
    [window.blit(menu[x], (y * SIZE_C, 0 * SIZE_R)) for x, y in (("start flag", 0), ("end flag", 3), ("wall", 6), ("start", 9))]


def draw_square():
    for row in range(ROW):
        for col in range(COL):
            window.blit(PICTURES[puzzel_field[row][col].picture], (col * SIZE_C, row * SIZE_R))
    draw_menu()
    if selected_button:
        selected_menu(*selected_button)


re_scale_all_pictures()

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
        if symbol.name == "BLANK":
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click, _, right_click = pygame.mouse.get_pressed()
            print(row, col)
            if row in (0, 1):
                if col in (0, 1):
                    menu["selected"]["start"] = True
                    selected_button = ("start flag", 1)
                    menu["selected"]["end"] = False

                elif col in (3, 4) and not menu["selected"]["end"]:
                    menu["selected"]["end"] = True
                    selected_button = ("end flag", 4)
                    menu["selected"]["start"] = False

            elif left_click and menu["selected"]["start"]:
                symbol.position_add(symbol, "start coordinates", "square_start_point")

            elif left_click and menu["selected"]["end"]:
                symbol.position_add(symbol, "exit coordinates", "square_end_point")

        elif event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                symbol.wall()

            elif key[pygame.K_UP]:
                if all(x for x in matrix_pos.values()):
                    search_for_exit(*matrix_pos["start coordinates"].position)
                print(way_to_unlock)


    draw_square()
    pygame.display.update()
pygame.quit()
