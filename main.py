import chess
import chess.svg
import pygame
import cairosvg
import io

# Size Constants
SCREEN_SIZE = 800 # (pixels)
BOARD_SIZE = 8 # (squares)
BOARD_MARGIN = 25 # (pixels)
SQUARE_SIZE = (SCREEN_SIZE - 2 * BOARD_MARGIN) // BOARD_SIZE # 100 (pixels)

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

# Global Variables
running = True
mouse_dragging = False
dragging_piece = None
mouse_x, mouse_y = None, None
start_square, end_square = None, None
make_move = False

# Chess Setup
board = chess.Board()

# It seems like Pygame's SVG loading is not working so I have to convert the SVG to PNG first
# SVG Loading
def load_svg(path):
    new_bites = cairosvg.svg2png(url=path)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io).convert()

with open('board.svg', 'w') as tmp:
    tmp.write(chess.svg.board(board, size=SCREEN_SIZE))

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]: # Left Mouse Button
                if not mouse_dragging:
                    file_index, rank_index = (mouse_x - BOARD_MARGIN) // SQUARE_SIZE, 7 - (mouse_y - BOARD_MARGIN) // SQUARE_SIZE
                    start_square = chess.square(file_index, rank_index)
                    dragging_piece = board.piece_at(start_square)
                mouse_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if not pygame.mouse.get_pressed()[0]: # Same
                file_index, rank_index = (mouse_x - BOARD_MARGIN) // SQUARE_SIZE, 7 - (mouse_y - BOARD_MARGIN) // SQUARE_SIZE
                end_square = chess.square(file_index, rank_index)
                make_move = True
                mouse_x = mouse_y = None
                mouse_dragging = False
                dragging_piece = None
    
    if make_move:
        # Make a Move
        try:
            board.push_uci(chess.square_name(start_square) + chess.square_name(end_square))
            print(chess.square_name(start_square) + chess.square_name(end_square), 'is a valid move')
        except: print(chess.square_name(start_square) + chess.square_name(end_square), 'is an invalid move')
    
    screen.fill('black')
    
    # Actual Drawing Starts
    
    if make_move:
        with open('board.svg', 'w') as tmp:
            tmp.write(chess.svg.board(board, size=SCREEN_SIZE))
        make_move = False
    # surface = pygame.image.load('board.svg').convert()
    surface = load_svg('board.svg').convert()
    screen.blit(surface, (0, 0))
    
    # if dragging_piece:
    #     with open('piece.svg', 'w') as tmp:
    #         tmp.write(chess.svg.piece(dragging_piece, size=SQUARE_SIZE))
    #     surface = pygame.image.load('piece.svg').convert()
    #     # surface = load_svg('piece.svg')
    #     screen.blit(surface, (mouse_x - SQUARE_SIZE / 2, mouse_y - SQUARE_SIZE / 2))
    
    # Actual Drawing Ends
    
    pygame.display.flip()

pygame.quit()