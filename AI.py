import pygame
# initialise pygame
pygame.init()
fps = 30
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Noughts and crosses")
# setup images
n = pygame.image.load('n.png').convert()
x = pygame.image.load('x.png').convert()
o = pygame.image.load('o.png').convert()
# game setup
board = [[n]*3, [n]*3, [n]*3]
tie = None
player = x
if player == o:
    bot = x
else:
    bot = o
moves = []


def draw_board():
    for i in range(len(board)):
        for j in range(len(board[i])):
            x = j*200
            y = i*200
            screen.blit(board[i][j], (x, y))


def bot_move():
    global n, count
    best_score = -800
    best_i = 0
    best_j = 0
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == n:
                board[i][j] = bot
                score = minimax(board, False)
                board[i][j] = n
                if score > best_score:
                    best_score = score
                    best_i = i
                    best_j = j
    print(count)
    board[best_i][best_j] = bot


def minimax(board, is_max,):
    global count
    count += 1
    if check_win(bot):
        return 1
    elif check_win(player):
        return -1
    elif check_draw():
        return 0
    if is_max:
        best_score = -800
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == n:
                    board[i][j] = bot
                    score = minimax(board, False)
                    board[i][j] = n
                    if score > best_score:
                        best_score = score
        return best_score
    else:
        best_score = 800
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == n:
                    board[i][j] = player
                    score = minimax(board, True)
                    board[i][j] = n
                    if score < best_score:
                        best_score = score
        return best_score


def check_click():
    global running
    # get the current state of the mouse buttons
    mouse_buttons = pygame.mouse.get_pressed()
    for i in range(len(board)):
        for j in range(len(board[i])):
            hitbox = pygame.Rect(j*200, i*200, 200, 200)
            if mouse_buttons[0] and board[i][j] == n and hitbox.collidepoint(pygame.mouse.get_pos()):
                board[i][j] = player
                if check_win(player):
                    print("Player wins")
                    running = False
                    break
                elif check_draw():
                    print("It is a draw.")
                    running = False
                    break
                bot_move()
                if check_win(bot):
                    print("Bot wins!")
                    running = False
                elif check_draw():
                    print("It is a draw.")
                    running = False


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
    if board[0][0] == board[1][1] == board[2][2] == turn or board[0][2] == board[1][1] == board[2][0] == turn:
        return True
    return False


def check_draw():
    global n
    for i in range(len(board)):
        if n in board[i]:
            return False
    return True


if bot == o:
    bot_move()
# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    check_click()
    draw_board()
    pygame.display.update()
    pygame.time.delay(1000 // fps)  # delay to control frame rate

pygame.quit()
