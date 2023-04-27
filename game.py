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
turn = o


def draw_board():
    for i in range(len(board)):
        for j in range(len(board[i])):
            x = j*200
            y = i*200
            screen.blit(board[i][j], (x, y))


def check_click():
    global turn, running
    # get the current state of the mouse buttons
    mouse_buttons = pygame.mouse.get_pressed()
    for i in range(len(board)):
        for j in range(len(board[i])):
            hitbox = pygame.Rect(j*200, i*200, 200, 200)
            if mouse_buttons[0] and board[i][j] == n and hitbox.collidepoint(pygame.mouse.get_pos()):
                board[i][j] = turn
                if check_win():
                    if turn == o:
                        print("Noughts wins!")
                    else:
                        print("Crosses wins!")
                    running = False
                elif check_draw():
                    print("It is a draw.")
                    running = False
                if turn == o:
                    turn = x
                else:
                    turn = o


def check_win():
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
