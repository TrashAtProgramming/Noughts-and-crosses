import pygame
import pygame_gui

# initialise pygame
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Noughts and crosses")
blue_manager = pygame_gui.UIManager((800, 600), "blue_button.json")
red_manager = pygame_gui.UIManager((800, 600), "red_button.json")
clock = pygame.time.Clock()
# setup images
n = pygame.image.load("n.png").convert()
x = pygame.image.load("x.png").convert()
o = pygame.image.load("o.png").convert()
font = pygame.font.SysFont("Arial", 72)


def draw_board():
    for i in range(len(board)):
        for j in range(len(board[i])):
            x = j * 200
            y = i * 200
            screen.blit(board[i][j], (x, y))


def bot_move():
    global n
    best_score = -800
    best_i = 0
    best_j = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == n:
                board[i][j] = bot
                score = minimax(board, False, -1000, +1000)
                board[i][j] = n
                if score > best_score:
                    best_score = score
                    best_i = i
                    best_j = j
    board[best_i][best_j] = bot


def minimax(board, is_max, alpha, beta):
    if check_win(bot):
        return 1
    elif check_win(player):
        return -1
    elif check_draw():
        return 0
    if is_max:
        best_score = -1000
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == n:
                    board[i][j] = bot
                    score = minimax(board, False, alpha, beta)
                    board[i][j] = n
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break
            if alpha >= beta:
                break
        return best_score
    else:
        best_score = 1000
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == n:
                    board[i][j] = player
                    score = minimax(board, True, alpha, beta)
                    board[i][j] = n
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        break
            if alpha >= beta:
                break
        return best_score


def check_click():
    global running, player, font
    # get the current state of the mouse buttons
    mouse_buttons = pygame.mouse.get_pressed()
    for i in range(len(board)):
        for j in range(len(board[i])):
            hitbox = pygame.Rect(j * 200, i * 200, 200, 200)
            if (
                mouse_buttons[0]
                and board[i][j] == n
                and hitbox.collidepoint(pygame.mouse.get_pos())
            ):
                board[i][j] = player
                if players == 1:
                    bot_move()
                    if check_win(bot):
                        message = "Bot wins!"
                        running = False
                    elif check_draw():
                        message = "It is a draw."
                        running = False
                    else:
                        message = ""
                else:
                    if check_win(player):
                        if player == x:
                            winner = "Crosses"
                        else:
                            winner = "Noughts"
                        message = f"{winner} wins!"
                        running = False
                    elif check_draw():
                        message = "It is a draw."
                        running = False
                    else:
                        message = ""
                    if player == o:
                        player = x
                    else:
                        player = o
                if message:
                    # create a text message
                    box_surface = pygame.Surface((400, 100))
                    box_surface.fill((255, 255, 255))
                    pygame.draw.rect(box_surface, (0, 0, 0), box_surface.get_rect(), 2)
                    message_display = font.render(message, True, (0, 0, 0))
                    draw_board()
                    screen.blit(box_surface, (100, 200))
                    screen.blit(message_display, (100, 200))
                    pygame.display.update()
                    pygame.time.wait(2000)


def title():
    # Create the text surfaces
    noughts_text = font.render("Noughts", True, (255, 0, 0))
    and_text = font.render("and", True, (0, 0, 0))
    crosses_text = font.render("Crosses", True, (0, 0, 255))

    # Get the dimensions of the text surfaces
    noughts_width, noughts_height = noughts_text.get_size()
    and_width, and_height = and_text.get_size()
    crosses_width, crosses_height = crosses_text.get_size()

    # Calculate the position of the text
    text_x = (width - noughts_width - and_width - crosses_width - 20) // 2
    text_y = (height - noughts_height) // 4

    # Create the box surface
    box_width = noughts_width + and_width + crosses_width + 40
    box_height = noughts_height + 20
    box_surface = pygame.Surface((box_width, box_height))
    box_surface.fill((255, 255, 255))
    pygame.draw.rect(box_surface, (0, 0, 0), box_surface.get_rect(), 2)

    # Blit the text and box surfaces to the screen
    screen.blit(box_surface, (text_x - 10, text_y - 10))
    screen.blit(noughts_text, (text_x, text_y))
    screen.blit(and_text, (text_x + noughts_width + 10, text_y))
    screen.blit(crosses_text, (text_x + noughts_width + and_width + 20, text_y))


def check_win(turn):
    # check row
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] == turn:
            return True
    # check column
    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] == turn:
            return True
    # check diagonals
    if (
        board[0][0] == board[1][1] == board[2][2] == turn
        or board[0][2] == board[1][1] == board[2][0] == turn
    ):
        return True
    return False


def check_draw():
    global n
    for i in range(len(board)):
        if n in board[i]:
            return False
    return True


def menu_setup():
    global players
    draw_board()
    title()
    menu = True
    while menu:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == two_player:
                    menu = False
                    players = 2
                if event.ui_element == one_player:
                    menu = False
                    players = 1
            blue_manager.process_events(event)
            red_manager.process_events(event)
        blue_manager.update(time_delta)
        red_manager.update(time_delta)
        blue_manager.draw_ui(screen)
        red_manager.draw_ui(screen)
        pygame.display.update()


# menu setup
two_player = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 250), (200, 100)),
    text="Two player",
    manager=blue_manager,
)
one_player = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 250), (200, 100)),
    text="One player",
    manager=red_manager,
)
players = 0
while True:
    running = True
    board = [[n] * 3, [n] * 3, [n] * 3]
    menu_setup()
    player = x
    if player == o:
        bot = x
    else:
        bot = o
    moves = []
    if bot == o and players == 1:
        bot_move()
    # game loop
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        check_click()
        draw_board()
        pygame.display.update()
