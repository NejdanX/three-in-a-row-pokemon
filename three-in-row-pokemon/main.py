""" 
                                    ИГРА ТРИ В РЯД
Игра заканчивается, если не остаётся доступных ходов или пока пользователь сам не прервёт игру.
В левом нижнем углу находятся очки, которые уменьшаются со временем. Цель игры в том, чтобы
как можно быстрее находить 3 (или более) одинаковых фигур в ряд и набирать очки. 
"""

import os
import random
import time
import sys
import copy
import pygame
import pygame.locals as locals
from Constants import *

timer = 0
background_number = 0
GAMEBACKGROUND = f'game_fon{background_number}.gif'


def run_game():
    global timer, background_number, GAMEBACKGROUND
    """Играем, пока не закроется окно или не останется доступных ходов"""
    game_board = get_blank_board()
    score = 0
    fill_board_and_animate(game_board, [], score)
    # инициализуем переменные для новой игры
    first_selected_pokemon = None
    last_mouse_down_x = None
    last_mouse_down_y = None
    game_is_over = False
    is_write_in_file = False
    string_rendered = ''
    last_score_deduction = time.time()
    click_continue_text_surf = None
    while True:  # главный цикл игры
        # Меняем фон раз в 60 секунд
        if pygame.time.get_ticks() // 1000 - timer > 60:
            timer = pygame.time.get_ticks() // 1000
            background_number = (background_number + 1) % 4
            GAMEBACKGROUND = f'game_fon{background_number}.gif'
        clicked_space = None
        for event in pygame.event.get():
            if event.type == locals.QUIT or (event.type == locals.KEYUP and event.key == locals.K_ESCAPE):
                main()
            elif event.type == locals.KEYUP and event.key == locals.K_BACKSPACE:
                return
            elif event.type == locals.MOUSEBUTTONUP:
                if game_is_over:
                    main()
                if event.pos == (last_mouse_down_x, last_mouse_down_y):
                    clicked_space = check_for_pokemon_click(event.pos)
                else:
                    first_selected_pokemon = check_for_pokemon_click((last_mouse_down_x, last_mouse_down_y))
                    clicked_space = check_for_pokemon_click(event.pos)
                    if not first_selected_pokemon or not clicked_space:
                        first_selected_pokemon = None
                        clicked_space = None
            elif event.type == locals.MOUSEBUTTONDOWN:
                last_mouse_down_x, last_mouse_down_y = event.pos

        if clicked_space and not first_selected_pokemon:
            first_selected_pokemon = clicked_space
        elif clicked_space and first_selected_pokemon:
            first_swapping_pokemon, second_swapping_pokemon = get_swapping_pokemons(game_board, first_selected_pokemon,
                                                                                    clicked_space)
            if first_swapping_pokemon is None and second_swapping_pokemon is None:
                first_selected_pokemon = None
                continue

            board_copy = getboard_copy_minus_pokemons(game_board, (first_swapping_pokemon, second_swapping_pokemon))
            animate_moving_pokemons(board_copy, [first_swapping_pokemon, second_swapping_pokemon], [], score)

            game_board[first_swapping_pokemon['x']][first_swapping_pokemon['y']] = second_swapping_pokemon['imageNum']
            game_board[second_swapping_pokemon['x']][second_swapping_pokemon['y']] = first_swapping_pokemon['imageNum']

            matched_pokemons = find_matching_pokemons(game_board)
            if not matched_pokemons:
                GAME_SOUNDS['bad swap'].play()
                animate_moving_pokemons(board_copy, [first_swapping_pokemon, second_swapping_pokemon], [], score)
                game_board[first_swapping_pokemon['x']][first_swapping_pokemon['y']] = \
                    first_swapping_pokemon['imageNum']
                game_board[second_swapping_pokemon['x']][second_swapping_pokemon['y']] = \
                    second_swapping_pokemon['imageNum']
            else:
                score_add = 0
                while matched_pokemons:
                    points = []
                    for pokemon_set in matched_pokemons:
                        score_add += (10 + (len(pokemon_set) - 3) * 10)
                        for pokemon in pokemon_set:
                            game_board[pokemon[0]][pokemon[1]] = EMPTY_SPACE
                        points.append({'points': score_add,
                                       'x': pokemon[0] * POKEMON_IMAGE_SIZE + X_MARGIN,
                                       'y': pokemon[1] * POKEMON_IMAGE_SIZE + Y_MARGIN})
                    random.choice(GAME_SOUNDS['match']).play()
                    score += score_add

                    fill_board_and_animate(game_board, points, score)

                    matched_pokemons = find_matching_pokemons(game_board)
            first_selected_pokemon = None

            if not can_make_move(game_board):
                game_is_over = True
        background = pygame.transform.scale(load_image(GAMEBACKGROUND), (600, 600))
        SCREEN.blit(background, (0, 0))
        draw_board(game_board)
        if first_selected_pokemon is not None:
            highlight_space(first_selected_pokemon['x'], first_selected_pokemon['y'])
        if game_is_over:
            with open('data/three_best_score.txt', 'r', encoding='utf8') as file:
                scores = list(map(str.strip, file.readlines()))
            if click_continue_text_surf is None:
                font = pygame.font.Font('freesansbold.ttf', 24)
                GAME_SOUNDS['complete'].play()
                string_points = f'Вы набрали: {score} очков(Нажмите любую кнопку)'
                click_continue_text_surf = font.render(string_points, True, GAMEOVER_COLOR, GAMEOVER_BGCOLOR)
                click_continue_text_rect = click_continue_text_surf.get_rect()
                click_continue_text_rect.center = int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2)
            background = pygame.transform.scale(load_image(END_BACKGROUND), (600, 600))
            text_coord = 400
            SCREEN.blit(background, (0, 0))
            for line in scores:
                string_rendered = font.render(line, True, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                SCREEN.blit(string_rendered, intro_rect)
            SCREEN.blit(click_continue_text_surf, click_continue_text_rect)
            if not is_write_in_file:
                is_write_in_file = True
                set_best_score_in_file(score)
            if event.type == locals.MOUSEBUTTONDOWN:
                main()
        elif score > 0 and time.time() - last_score_deduction > DEDUCT_SPEED:
            # очки постоянно уменьшаются
            score -= 1
            last_score_deduction = time.time()
        draw_score(score)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def set_best_score_in_file(score):
    with open('data/three_best_score.txt', 'r', encoding='utf8') as read_file:
        lines = list(map(str.strip, read_file.readlines()))
        if lines:
            for index, line in enumerate(lines):
                if int(line.split()[-1]) < score:
                    lines.insert(index, f'{index + 1} место: {score}')
                    with open('data/three_best_score.txt', 'w', encoding='utf8') as write_in_file:
                        write_in_file.write('\n'.join(lines[:3]) + '\n')
                        break
                elif len(lines) != 3:
                    with open('data/three_best_score.txt', 'a', encoding='utf8') as write_in_file:
                        write_in_file.write(f'{len(lines) + 1} место: {score}\n')
        else:
            with open('data/three_best_score.txt', 'w', encoding='utf8') as write_in_file:
                write_in_file.write(f'1 место: {score}\n')


def get_swapping_pokemons(board, first_xy, second_xy):
    first_pokemon = {'imageNum': board[first_xy['x']][first_xy['y']],
                     'x': first_xy['x'],
                     'y': first_xy['y']}
    second_pokemon = {'imageNum': board[second_xy['x']][second_xy['y']],
                      'x': second_xy['x'],
                      'y': second_xy['y']}
    if first_pokemon['x'] == second_pokemon['x'] + 1 and first_pokemon['y'] == second_pokemon['y']:
        first_pokemon['direction'] = LEFT
        second_pokemon['direction'] = RIGHT
    elif first_pokemon['x'] == second_pokemon['x'] - 1 and first_pokemon['y'] == second_pokemon['y']:
        first_pokemon['direction'] = RIGHT
        second_pokemon['direction'] = LEFT
    elif first_pokemon['y'] == second_pokemon['y'] + 1 and first_pokemon['x'] == second_pokemon['x']:
        first_pokemon['direction'] = UP
        second_pokemon['direction'] = DOWN
    elif first_pokemon['y'] == second_pokemon['y'] - 1 and first_pokemon['x'] == second_pokemon['x']:
        first_pokemon['direction'] = DOWN
        second_pokemon['direction'] = UP
    else:
        # Не смогли свапнуть
        return None, None
    return first_pokemon, second_pokemon


def get_blank_board():
    board = []
    for x in range(BOARD_WIDTH):
        board.append([EMPTY_SPACE] * BOARD_HEIGHT)
    return board


def can_make_move(board):
    one_off_patterns = (((0, 1), (1, 0), (2, 0)),
                        ((0, 1), (1, 1), (2, 0)),
                        ((0, 0), (1, 1), (2, 0)),
                        ((0, 1), (1, 0), (2, 1)),
                        ((0, 0), (1, 0), (2, 1)),
                        ((0, 0), (1, 1), (2, 1)),
                        ((0, 0), (0, 2), (0, 3)),
                        ((0, 0), (0, 1), (0, 3)))

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            for pat in one_off_patterns:
                # проверяем, может ли мы куда-то походить
                if (get_pokemon_at(board, x + pat[0][0], y + pat[0][1]) ==
                    get_pokemon_at(board, x + pat[1][0], y + pat[1][1]) ==
                    get_pokemon_at(board, x + pat[2][0], y + pat[2][1]) is not None) or \
                        (get_pokemon_at(board, x + pat[0][1], y + pat[0][0]) ==
                         get_pokemon_at(board, x + pat[1][1], y + pat[1][0]) ==
                         get_pokemon_at(board, x + pat[2][1], y + pat[2][0]) is not None):
                    return True
    return False


def draw_moving_pokemon(pokemon, progress):
    """Осуществляет анимацию движения кристаллов"""
    move_x = 0
    move_y = 0
    progress *= 0.01

    if pokemon['direction'] == UP:
        move_y = -int(progress * POKEMON_IMAGE_SIZE)
    elif pokemon['direction'] == DOWN:
        move_y = int(progress * POKEMON_IMAGE_SIZE)
    elif pokemon['direction'] == RIGHT:
        move_x = int(progress * POKEMON_IMAGE_SIZE)
    elif pokemon['direction'] == LEFT:
        move_x = -int(progress * POKEMON_IMAGE_SIZE)

    base_x = pokemon['x']
    base_y = pokemon['y']
    if base_y == ROW_ABOVE_BOARD:
        base_y = -1

    pixel_x = X_MARGIN + (base_x * POKEMON_IMAGE_SIZE)
    pixel_y = Y_MARGIN + (base_y * POKEMON_IMAGE_SIZE)
    r = pygame.Rect((pixel_x + move_x, pixel_y + move_y, POKEMON_IMAGE_SIZE, POKEMON_IMAGE_SIZE))
    SCREEN.blit(POKEMON_IMAGES[pokemon['imageNum']], r)


def pull_down_all_pokemons(board):
    """Заполняет доску, чтобы заполнить пробелы"""
    for x in range(BOARD_WIDTH):
        pokemons_in_column = []
        for y in range(BOARD_HEIGHT):
            if board[x][y] != EMPTY_SPACE:
                pokemons_in_column.append(board[x][y])
        board[x] = ([EMPTY_SPACE] * (BOARD_HEIGHT - len(pokemons_in_column))) + pokemons_in_column


def get_pokemon_at(board, x, y):
    if x < 0 or y < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
        return None
    else:
        return board[x][y]


def get_drop_slots(board):
    board_copy = copy.deepcopy(board)
    pull_down_all_pokemons(board_copy)

    drop_slots = []
    for i in range(BOARD_WIDTH):
        drop_slots.append([])

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT - 1, -1, -1):
            if board_copy[x][y] == EMPTY_SPACE:
                possible_pokemons = list(range(len(POKEMON_IMAGES)))
                for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    neighbor_pokemon = get_pokemon_at(board_copy, x + offsetX, y + offsetY)
                    if neighbor_pokemon is not None and neighbor_pokemon in possible_pokemons:
                        possible_pokemons.remove(neighbor_pokemon)

                new_pokemon = random.choice(possible_pokemons)
                board_copy[x][y] = new_pokemon
                drop_slots[x].append(new_pokemon)
    return drop_slots


def find_matching_pokemons(board):
    pokemons_to_remove = []
    board_copy = copy.deepcopy(board)

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if get_pokemon_at(board_copy, x, y) == get_pokemon_at(board_copy, x + 1, y) == \
                    get_pokemon_at(board_copy, x + 2, y) and get_pokemon_at(board_copy, x, y) != EMPTY_SPACE:
                target_pokemon = board_copy[x][y]
                offset = 0
                remove_set = []
                while get_pokemon_at(board_copy, x + offset, y) == target_pokemon:
                    remove_set.append((x + offset, y))
                    board_copy[x + offset][y] = EMPTY_SPACE
                    offset += 1
                pokemons_to_remove.append(remove_set)

            if get_pokemon_at(board_copy, x, y) == get_pokemon_at(board_copy, x, y + 1) == \
                    get_pokemon_at(board_copy, x, y + 2) and get_pokemon_at(board_copy, x, y) != EMPTY_SPACE:
                target_pokemon = board_copy[x][y]
                offset = 0
                remove_set = []
                while get_pokemon_at(board_copy, x, y + offset) == target_pokemon:
                    remove_set.append((x, y + offset))
                    board_copy[x][y + offset] = EMPTY_SPACE
                    offset += 1
                pokemons_to_remove.append(remove_set)

    return pokemons_to_remove


def highlight_space(x, y):
    pygame.draw.rect(SCREEN, HIGHLIGHT_COLOR, BOARD_RECTS[x][y], 4)


def get_dropping_pokemons(board):
    board_copy = copy.deepcopy(board)
    dropping_pokemons = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT - 2, -1, -1):
            if board_copy[x][y + 1] == EMPTY_SPACE and board_copy[x][y] != EMPTY_SPACE:
                dropping_pokemons.append({'imageNum': board_copy[x][y], 'x': x, 'y': y, 'direction': DOWN})
                board_copy[x][y] = EMPTY_SPACE
    return dropping_pokemons


def animate_moving_pokemons(board, pokemons, points_text, score):
    progress = 0
    while progress < 100:
        background = pygame.transform.scale(load_image(GAMEBACKGROUND), (600, 600))
        SCREEN.blit(background, (0, 0))
        draw_board(board)
        for pokemon in pokemons:
            draw_moving_pokemon(pokemon, progress)
        draw_score(score)
        for point_text in points_text:
            points_surf = BASIC_FONT.render(str(point_text['points']), True, SCORE_COLOR)
            points_rect = points_surf.get_rect()
            points_rect.center = (point_text['x'], point_text['y'])
            SCREEN.blit(points_surf, points_rect)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        progress += MOVE_RATE


def move_pokemons(board, moving_pokemons):
    for pokemon in moving_pokemons:
        if pokemon['y'] != ROW_ABOVE_BOARD:
            board[pokemon['x']][pokemon['y']] = EMPTY_SPACE
            move_x = 0
            move_y = 0
            if pokemon['direction'] == LEFT:
                move_x = -1
            elif pokemon['direction'] == RIGHT:
                move_x = 1
            elif pokemon['direction'] == DOWN:
                move_y = 1
            elif pokemon['direction'] == UP:
                move_y = -1
            board[pokemon['x'] + move_x][pokemon['y'] + move_y] = pokemon['imageNum']
        else:
            board[pokemon['x']][0] = pokemon['imageNum']


def fill_board_and_animate(board, points, score):
    drop_slots = get_drop_slots(board)
    while drop_slots != [[]] * BOARD_WIDTH:
        moving_pokemons = get_dropping_pokemons(board)
        for x in range(len(drop_slots)):
            if len(drop_slots[x]) != 0:
                moving_pokemons.append({'imageNum': drop_slots[x][0], 'x': x, 'y': ROW_ABOVE_BOARD, 'direction': DOWN})

        board_copy = getboard_copy_minus_pokemons(board, moving_pokemons)
        animate_moving_pokemons(board_copy, moving_pokemons, points, score)
        move_pokemons(board, moving_pokemons)

        for x in range(len(drop_slots)):
            if len(drop_slots[x]) == 0:
                continue
            board[x][0] = drop_slots[x][0]
            del drop_slots[x][0]


def check_for_pokemon_click(pos):
    """Проверяем, где кликнул пользователь (в поле или нет)"""
    if pos and len(pos) == 2 and pos[0] and pos[1]:
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if BOARD_RECTS[x][y].collidepoint(pos[0], pos[1]):
                    return {'x': x, 'y': y}
    return None


def draw_board(board):
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            pygame.draw.rect(SCREEN, GRID_COLOR, BOARD_RECTS[x][y], 1)
            pokemon_to_draw = board[x][y]
            if pokemon_to_draw != EMPTY_SPACE:
                SCREEN.blit(POKEMON_IMAGES[pokemon_to_draw], BOARD_RECTS[x][y])


def getboard_copy_minus_pokemons(board, pokemons):
    board_copy = copy.deepcopy(board)
    for pokemon in pokemons:
        if pokemon['y'] != ROW_ABOVE_BOARD:
            board_copy[pokemon['x']][pokemon['y']] = EMPTY_SPACE
    return board_copy


def draw_score(score):
    score_img = BASIC_FONT.render(f'Очки: {score}', True, SCORE_COLOR)
    score_rect = score_img.get_rect()
    score_rect.bottomleft = (10, WINDOW_HEIGHT - 6)
    SCREEN.blit(score_img, score_rect)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    intro_text = ["ТРИ В РЯД С ПОКЕМОНАМИ", "",
                  "                                         ПРАВИЛА ",
                  "          Составляйте покемонов одного типа в один ряд ",
                  "          или столбик (исключая диагональ).",
                  "          Три и больше одинаковых тут же исчезают, ",
                  "          вызывая появление на поле новых.",
                  "          Чем больше в ряд или столбик поставлено ",
                  "          покемонов, тем больше очков вы получите.",
                  "                                  ПРИЯТНОЙ ИГРЫ!"]
    background = pygame.transform.scale(load_image(START_BACKGROUND), (600, 600))
    SCREEN.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    button2 = pygame.Rect(500, 500, 75, 50)
    button = pygame.Rect(350, 500, 75, 50)

    pygame.draw.rect(SCREEN, [40, 40, 180], button)
    pygame.draw.rect(SCREEN, [255, 0, 0], button2)
    start_string = font.render('Старт', True, pygame.Color('white'))
    rect_start_string = start_string.get_rect()
    rect_start_string.x += 358
    rect_start_string.y += 515
    SCREEN.blit(start_string, rect_start_string)
    exit_string = font.render('Выход', True, pygame.Color('white'))
    rect_exit_string = start_string.get_rect()
    rect_exit_string.x += 503
    rect_exit_string.y += 515
    SCREEN.blit(exit_string, rect_exit_string)
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        SCREEN.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    return  # начинаем игру
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button2.collidepoint(event.pos):
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)


def load_image(name):
    filename = 'data/Backgrounds/' + name
    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    image = pygame.image.load(filename)
    return image


def main():
    global FPS_CLOCK, SCREEN, POKEMON_IMAGES, GAME_SOUNDS, BASIC_FONT, BOARD_RECTS

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption('Три в ряд')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 32)
    # Подгружаем изображения
    POKEMON_IMAGES = []
    for i in range(1, NUM_POKEMON_IMAGES + 1):
        pokemon_image = pygame.image.load(f'data/Sprites/pokemon{i}.png')
        if pokemon_image.get_size() != (POKEMON_IMAGE_SIZE, POKEMON_IMAGE_SIZE):
            pokemon_image = pygame.transform.smoothscale(pokemon_image, (POKEMON_IMAGE_SIZE, POKEMON_IMAGE_SIZE))
        POKEMON_IMAGES.append(pokemon_image)

    # Подгружаем звуки
    GAME_SOUNDS = {}
    GAME_SOUNDS['bad swap'] = pygame.mixer.Sound('data/Music/badswap.mp3')
    GAME_SOUNDS['match'] = []
    GAME_SOUNDS['background'] = []
    for i in range(NUM_MATCH_SOUNDS):
        GAME_SOUNDS['match'].append(pygame.mixer.Sound(f'data/Music/match{i}.mp3'))
    for i in range(NUM_BACKGROUND_SONGS):
        GAME_SOUNDS['background'].append(pygame.mixer.Sound(f'data/Music/background{i}.mp3'))
    GAME_SOUNDS['complete'] = pygame.mixer.Sound('data/Music/complete.mp3')

    BOARD_RECTS = []
    for x in range(BOARD_WIDTH):
        BOARD_RECTS.append([])
        for y in range(BOARD_HEIGHT):
            r = pygame.Rect((X_MARGIN + (x * POKEMON_IMAGE_SIZE),
                             Y_MARGIN + (y * POKEMON_IMAGE_SIZE),
                             POKEMON_IMAGE_SIZE,
                             POKEMON_IMAGE_SIZE))
            BOARD_RECTS[x].append(r)
    start_screen()
    while True:
        run_game()


if __name__ == '__main__':
    main()
