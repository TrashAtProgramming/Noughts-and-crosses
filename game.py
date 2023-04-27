import pygame

# initialise pygame
pygame.init()

fps = 30
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Noughts and crosses")

# set colours
white = (255, 255, 255)
black = (0, 0, 0)

# setup images
n = pygame.image.load('n.png').convert()
x = pygame.image.load('x.png').convert()
o = pygame.image.load('o.png').convert()

# game setup
board = [[n]*3, [n]*3, [n]*3]
winner = None
tie = None


def draw_board():
    for i in range(len(board)):
        for j in range(len(board[i])):
            x = j*200
            y = i*200
            screen.blit(board[i][j], (x, y))


# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_board()
    pygame.display.update()
    pygame.time.delay(1000 // fps)  # delay to control frame rate

pygame.quit()
