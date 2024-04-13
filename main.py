import pygame
import socket
import sys
from components.constant import *


def init_pygame():
    # Pygame initialization
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    return win


def draw_board(board, win):
    win.fill(WHITE)
    cell_width = WIDTH // len(board[0])  # Calculate cell width
    cell_height = HEIGHT // len(board)  # Calculate cell height
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            color = BLACK
            if cell == 'G':
                color = GREEN
            elif cell == 'Y':
                color = YELLOW
            elif cell == 'P':
                color = PINK
            elif cell == 'B':
                color = BLUE
            elif cell == 'F':
                color = RED
            pygame.draw.rect(win, color, (j * cell_width, i * cell_height, cell_width, cell_height))
    pygame.display.update()


def main():
    # Invoke pygame init function
    win = init_pygame()

    # Server connection
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER, PORT))
        client_socket.settimeout(0.1)  # Set timeout = 100ms
        size_data = client_socket.recv(4)
        board_size = int.from_bytes(size_data)
        board_mem = board_size ** 2

    except Exception as e:
        print("Błąd podczas łączenia z serwerem:", e)
        pygame.quit()
        sys.exit()

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    client_socket.send(b'U')
                elif event.key == pygame.K_DOWN:
                    client_socket.send(b'D')
                elif event.key == pygame.K_LEFT:
                    client_socket.send(b'L')
                elif event.key == pygame.K_RIGHT:
                    client_socket.send(b'R')

        try:
            data = client_socket.recv(board_mem)  # Receive 900 bytes, assuming a 30x30 board
            if data:
                decoded_data = data.decode('utf-8')
                # Create list of lists from received string
                board = [list(decoded_data[i:i + board_size]) for i in range(0, board_mem, board_size)]
                draw_board(board, win)

        except socket.timeout:
            print("Socket timeout")
            break
        except Exception as e:
            print("Błąd podczas odbierania danych:", e)
            break

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
