import socket
import random
import json

host = "localhost"
port = 7777
banner = """
=== Guessing Game ===
Choose difficulty level:    
a - Easy (1-50)
b - Medium (1-100)
c - Hard (1-300)
Enter the letter then press 'Enter' two times:
"""

def generate_random_int(difficulty):
    if difficulty == 'a':
        return random.randint(1, 50)
    elif difficulty == 'b':
        return random.randint(1, 100)
    elif difficulty == 'c':
        return random.randint(1, 300)

def update_leaderboard(name, score, difficulty, leaderboard):
    leaderboard.append({"name": name, "score": score, "difficulty": difficulty})
    leaderboard.sort(key=lambda x: x["score"])
    return leaderboard[:10]

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

leaderboard = load_leaderboard()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print(f"Server started on {host}:{port}")

while True:
    client_socket, client_address = server.accept()
    print(f"Connection from {client_address}")
    client_socket.sendall(banner.encode())

    try:
        difficulty = client_socket.recv(1024).decode().strip()
        target = generate_random_int(difficulty)
        attempts = 0

        while True:
            guess = client_socket.recv(1024).decode().strip()
            if not guess:
                break

            attempts += 1
            guess = int(guess)

            if guess < target:
                client_socket.sendall(b"Higher")
            elif guess > target:
                client_socket.sendall(b"Lower")
            else:
                client_socket.sendall(b"Correct")
                client_socket.sendall(b"Enter your name: ")
                name = client_socket.recv(1024).decode().strip()
                leaderboard = update_leaderboard(name, attempts, difficulty, leaderboard)
                save_leaderboard(leaderboard)
                break
    except ConnectionResetError:
        print("Client disconnected unexpectedly.")
    finally:
        client_socket.close()
