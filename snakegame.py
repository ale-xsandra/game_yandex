import pygame
import sys
import random


# размер экрана
weidth, height = 800, 600
background_color = (0, 0, 0)
block_size = 15

wall_blocks = 3
wall_color = (31, 31, 31)

text_color = (255, 255, 255)
font_size = int(wall_blocks * block_size * 0.75)

# размер поля
size_x = weidth // block_size - wall_blocks * 2
size_y = height // block_size - wall_blocks * 2

# скорость смены кадров
initial_game_speed = 3
speed_up = 1.05

apples = 3
apple_color = (191, 31, 31)
apple_radius = block_size // 3

initial_snake_lenght = 3
snake_color = (31, 191, 31)
snake_radius = block_size // 4


def main():
    screen, clock = initialz_pygame()
    game_state = initialz_game_state()  # начальное состояние игры
    while game_state['prog_running']:
        clock.tick(game_state['game_speed'])
        # считываем и обрабатываем все события
        events = get_events(game_state)
        # изменяем game_state исходя из событий
        update_game_state(events, game_state)
        # смена изображения на экане
        update_screen(screen, game_state)
    perform_end()


def initialz_pygame():
    # инициализация pygame
    pygame.init()
    # выставляем размер игрового окна
    screen = pygame.display.set_mode((weidth, height))
    # меняем название
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    # подключение музыки
    pygame.mixer.music.load('/Users/Jenya/Downloads/game_yandex/personal_resume_presentation_pack/music_snake.mp3')
    pygame.mixer.music.play()

    return screen, clock


def initialz_game_state():
    game_state = {
        'prog_running': True,
        'game_running': False,
        'game_paused': False,
        'game_speed': initial_game_speed,
        'game_score': 0
    }
    return game_state


def get_events(game_state):
    events = []
    for event in pygame.event.get():
        if event == pygame.QUIT:
            game_state['prog_running'] = False
            events.append('quit')
        # провека нажатия кнопки, type - тип, key - занчение
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                events.append('up')
            if event.key == pygame.K_DOWN:
                events.append('down')
            if event.key == pygame.K_LEFT:
                events.append('left')
            if event.key == pygame.K_RIGHT:
                events.append('right')
            if event.key == pygame.K_SPACE:
                events.append('space')
            if event.key == pygame.K_RETURN:  # или enter
                events.append('return')
            if event.key == pygame.K_ESCAPE:
                events.append('escape')
    return events


def update_game_state(events, game_state):
    check_key_presses(events, game_state)
    if game_state['game_running'] and not game_state['game_paused']:
        # движение
        move_snake(game_state)
        # проверка на столкновение
        check_collisions(game_state)
        # проверка на потребление с яблоками
        check_apple_consumotion(game_state)


def move_snake(game_state):
    # координаты головы
    x = game_state['snake'][0][0] + game_state['direction'][0]
    y = game_state['snake'][0][1] + game_state['direction'][1]
    game_state['snake'].insert(0, (x, y))


def check_collisions(game_state):
    x, y = game_state['snake'][0]
    # проверка врезание в стену
    if x < 0 or y < 0 or x >= size_x or y >= size_y:
        game_state['game_running'] = False
    # проверка на столкновение с собой (длина будет больше, потому что 2 одинаковые коодринаты)
    if len(game_state['snake']) > len(set(game_state['snake'])):
        game_state['game_running'] = False


def check_apple_consumotion(game_state):
    apples_eat = 0
    for ap in game_state['apples']:
        # столкновение яблока с головой
        if ap == game_state['snake'][0]:
            # удаляем яблоко
            game_state['apples'].remove(ap)
            place_apples(1, game_state)
            game_state['game_score'] += 1
            apples_eat += 1
            # увеличиваем скорость на 10% с округлением до ближайшего целого числа
            game_state['game_speed'] = (game_state['game_speed'] * speed_up)
    if apples_eat == 0:
        game_state['snake'].pop()


def check_key_presses(events, game_state):
    if not game_state['game_running']:
        if 'escape' in events:
            game_state['game_running'] = False
        elif 'return' in events:
            initialz_new_game(game_state)
            game_state['game_running'] = True
    elif game_state['game_paused']:
        if 'escape' in events:
            game_state['game_paused'] = False
        elif 'space' in events:
            game_state['game_running'] = False
    else:
        if 'escape' in events or 'space' in events:
            game_state['game_paused'] = True
        if 'up' in events:
            game_state['direction'] = (0, -1)
        if 'down' in events:
            game_state['direction'] = (0, 1)
        if 'left' in events:
            game_state['direction'] = (-1, 0)
        if 'right' in events:
            game_state['direction'] = (1, 0)


def initialz_new_game(game_state):
    # положение змейки
    game_state['snake'] = []
    place_snake(initial_snake_lenght, game_state)
    # положение яброк
    game_state['apples'] = []
    place_apples(apples, game_state)
    # направление движения змейки
    game_state['direction'] = (1, 0)  # (x, y)
    # на паузе ли игра
    game_state['game_paused'] = False
    # сколько очков
    game_state['score'] = 0
    # скорость игры
    game_state['game_speed'] = initial_game_speed


def place_snake(lenght, game_state):
    # середина поля
    x = size_x // 2
    y = size_y // 2
    # голова
    game_state['snake'].append((x, y))
    # туловище
    for i in range(1, lenght - 1):
        game_state['snake'].append((x-i, y))


def place_apples(n, game_state):
    for i in range(n):
        # рандомные координаты для яблок
        x = random.randint(0, size_x - 1)
        y = random.randint(0, size_y - 1)
        while (x, y) in game_state['apples'] or (x, y) in game_state['snake']:
            # если условие выполняется, заново происходит генерация
            x = random.randint(0, size_x - 1)
            y = random.randint(0, size_y - 1)
        game_state['apples'].append((x, y))


def update_screen(screen, game_state):
    # задаем цвет экрана
    screen.fill(background_color)
    # вывод сообщений
    if not game_state['game_running']:
        print_new_game_message(screen)
    elif game_state['game_paused']:
        print_game_paused_message(screen)
    else:
        # отрисовка яблок, змеи
        draw_apples(screen, game_state['apples'])
        draw_snake(screen, game_state['snake'])
    # рисуем стены
    draw_walls(screen)
    # вывод очков
    print_score(screen, game_state['game_score'])
    # переворачиваем экран - показываем цвет экрана
    pygame.display.flip()


def draw_apples(screen, apple):
    for appl in apple:
        x = appl[0] * block_size + wall_blocks * block_size
        y = appl[1] * block_size + wall_blocks * block_size
        pygame.draw.rect(screen, apple_color, ((x, y), (block_size, block_size)), border_radius=apple_radius)


def print_new_game_message(screen):
    # настойка шрифта
    font = pygame.font.SysFont('Courier New', font_size, bold=True)
    text_new = font.render('Нажмите на ENTER, чтобы начать новую игру', True, text_color)
    text_restart = font.render('Нажмите на ESCAPE, чтобы выйти', True, text_color)
    # выстраивание положения текста
    text_rec_new = text_new.get_rect()
    text_rect_rest = text_restart.get_rect()
    text_rec_new.center = (weidth // 2, height // 2 - font_size // 2)
    text_rect_rest.center = (weidth // 2, height // 2 + font_size // 2)
    screen.blit(text_new, text_rec_new)
    screen.blit(text_restart, text_rect_rest)


def print_game_paused_message(screen):
    # настойка шрифта
    font = pygame.font.SysFont('Courier New', font_size, bold=True)
    text_continue = font.render('Нажмите на SPACE, чтобы продолжить', True, text_color)
    text_restart = font.render('Нажмите на ESCAPE, чтобы начать новую игру', True, text_color)
    # выстраивание положения текста
    text_rec_cont = text_continue.get_rect()
    text_rect_rest = text_restart.get_rect()
    text_rec_cont.center = (weidth // 2, height // 2 - font_size // 2)
    text_rect_rest.center = (weidth // 2, height // 2 + font_size // 2)
    screen.blit(text_continue, text_rec_cont)
    screen.blit(text_restart, text_rect_rest)


def draw_snake(screen, snake):
    for part in snake:
        x = part[0] * block_size + wall_blocks * block_size
        y = part[1] * block_size + wall_blocks * block_size
        pygame.draw.rect(screen, snake_color, ((x, y), (block_size, block_size)), border_radius=snake_radius)


def draw_walls(screen):
    wall_sz = wall_blocks * block_size
    pygame.draw.rect(screen, wall_color, ((0, 0), (weidth, wall_sz)))
    pygame.draw.rect(screen, wall_color, ((0, 0), (wall_sz, height)))
    pygame.draw.rect(screen, wall_color, ((0, height - wall_sz), (weidth, height)))
    pygame.draw.rect(screen, wall_color, ((weidth - wall_sz, 0), (weidth, height)))


def print_score(screen, score):
    wall_sz = wall_blocks * block_size
    font = pygame.font.SysFont('Courier New', font_size, bold=True)
    text = font.render('Счет: ' + str(score), True, text_color)
    text_rect = text.get_rect()
    text_rect.midleft = (wall_sz, wall_sz // 2)
    screen.blit(text, text_rect)


def perform_end():
    # конец игры
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()