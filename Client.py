import socket

host = "localhost"
port = 7777

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    try:
        data = s.recv(1024)
        if not data:
            print("Server disconnected.")
            break

        print(data.decode().strip())
        difficulty_choice = input("Enter difficulty: ").strip()
        s.sendall(difficulty_choice.encode())

        while True:
            user_input = input("Your guess: ").strip()
            if not user_input.isdigit():
                print("Please enter a valid number.")
                continue
            s.sendall(user_input.encode())
            reply = s.recv(1024).decode().strip()
            print(reply)
            if "Correct" in reply:
                name = input("Enter your name: ").strip()
                s.sendall(name.encode())
                break
    except ConnectionResetError:
        print("Server disconnected unexpectedly.")
        break
    finally:
        s.close()
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            break
