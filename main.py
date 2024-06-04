import socket
import threading

# Global variables to keep track of the game state and player turns
board = [' ' for _ in range(9)]
current_turn = 'X'
players = []
game_active = False


# Function to print the board
def print_board():
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("-+-+-")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("-+-+-")
    print(f"{board[6]}|{board[7]}|{board[8]}")


# Function to check for a win or tie
def check_game_status():
    global game_active
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != ' ':
            return board[condition[0]]

    if ' ' not in board:
        return 'Tie'

    return None


# Function to handle each client
def handle_client(conn, player):
    global current_turn, game_active
    conn.sendall("Welcome to Noughts and Crosses!\n".encode())
    conn.sendall("Waiting for another player...\n".encode())

    # Wait until both players have connected
    while len(players) < 2:
        pass

    conn.sendall(f"Game starting! You are {player}\n".encode())

    while game_active:
        conn.sendall(print_board().encode())

        if current_turn == player:
            conn.sendall("Your move (0-8): ".encode())
            move = int(conn.recv(1024).decode())

            if board[move] == ' ':
                board[move] = player
                current_turn = 'O' if player == 'X' else 'X'
            else:
                conn.sendall("Invalid move. Try again.\n".encode())

            status = check_game_status()
            if status:
                if status == 'Tie':
                    conn.sendall("It's a tie!\n".encode())
                else:
                    conn.sendall(f"Player {status} wins!\n".encode())
                game_active = False
        else:
            conn.sendall("Waiting for the other player...\n".encode())

    conn.sendall(print_board().encode())
    conn.close()


# Server setup
def start_server():
    global game_active
    game_active = True

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(2)
    print("Server started, waiting for players...")

    while len(players) < 2:
        conn, addr = server.accept()
        players.append(conn)
        player = 'X' if len(players) == 1 else 'O'
        threading.Thread(target=handle_client, args=(conn, player)).start()

    for player in players:
        player.sendall("Game starting!\n".encode())
