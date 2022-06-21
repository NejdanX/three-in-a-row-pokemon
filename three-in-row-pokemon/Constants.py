FPS = 30
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

BOARD_WIDTH = 8
BOARD_HEIGHT = 8
POKEMON_IMAGE_SIZE = 64
NUM_POKEMON_IMAGES = 7  # количество типов кристаллов

NUM_MATCH_SOUNDS = 4  # количество типов звуков
NUM_BACKGROUND_SONGS = 4

MOVE_RATE = 25  # скорость анимации падения кристаллов
DEDUCT_SPEED = 0.8

PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
RED = (255, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HIGHLIGHT_COLOR = RED  # цвет выделение выбранной ячейки
GRID_COLOR = BLACK  # цвет сетки
GAMEOVER_COLOR = WHITE  # цвет надписи "Game Over"
GAMEOVER_BGCOLOR = BLACK  # фон окончания игры
SCORE_COLOR = (255, 255, 255)  # цвет очков набранных игроком
START_BACKGROUND = 'start_background.jpg'
END_BACKGROUND = 'end_background.jpg'

# Отступы
X_MARGIN = int((WINDOW_WIDTH - POKEMON_IMAGE_SIZE * BOARD_WIDTH) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - POKEMON_IMAGE_SIZE * BOARD_HEIGHT) / 2)

# Константы направлений
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

EMPTY_SPACE = -1
ROW_ABOVE_BOARD = 'row above board'
