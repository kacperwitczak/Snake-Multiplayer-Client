import pygame
import socket
import sys

# Ustawienia serwera
SERVER = "127.0.0.1"
PORT = 8888

# Rozmiar okna gry
WIDTH, HEIGHT = 600, 600

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicjalizacja Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

def draw_board(board):
    win.fill(WHITE)
    cell_width = WIDTH // len(board[0])  # Oblicz szerokość komórki
    cell_height = HEIGHT // len(board)  # Oblicz wysokość komórki
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            color = BLACK
            if cell == 'H':
                color = GREEN
            elif cell == 'B':
                color = BLUE
            elif cell == 'F':
                color = RED
            pygame.draw.rect(win, color, (j * cell_width, i * cell_height, cell_width, cell_height))
    pygame.display.update()

# Połączenie z serwerem
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))
    client_socket.settimeout(0.1)  # Ustaw timeout na 100 ms
except Exception as e:
    print("Błąd podczas łączenia z serwerem:", e)
    pygame.quit()
    sys.exit()

# Główna pętla gry
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
        data = client_socket.recv(900)  # Odbierz 900 bajtów, zakładając, że plansza jest rozmiaru 30x30
        if data:
            decoded_data = data.decode('utf-8')
            # Twórz listę list (planszę) z otrzymanego łańcucha znaków
            board = [list(decoded_data[i:i + 30]) for i in range(0, 900, 30)]
            draw_board(board)

    except socket.timeout:
        pass
    except Exception as e:
        print("Błąd podczas odbierania danych:", e)
        break

    clock.tick(60)

pygame.quit()
