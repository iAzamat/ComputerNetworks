import socket
import threading
import configparser
import tkinter as tk
from tkinter import simpledialog, messagebox


def start_client():
    print(f"Start client")
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг

    # Connection Data
    host = config["Chat"]["host"]
    port = int(config["Chat"]["port"])

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    root = tk.Tk()
    root.title("Chat Application")

    chat_window = tk.Text(root)
    chat_window.pack()

    entry = tk.Entry(root)
    entry.pack()

    def get_username():
        username = simpledialog.askstring("Введите имя пользователя", "Введите ваше имя:")
        if username:
            return username
        else:
            tk.messagebox.showwarning("Внимание", "Вы не ввели имя пользователя!")
            get_username()

    # Choosing Nickname
    nickname = get_username()
    root.title(f"Chat Application. User: {nickname}")

    # Listening to Server and Sending Nickname
    def receive():
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    chat_window.insert(tk.END, f"{message}\n")
                    # print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                client.close()
                break

    def write():
        message = '{}: {}'.format(nickname, entry.get())
        client.send(message.encode('ascii'))
        # chat_window.insert(tk.END, f"{message}\n")
        entry.delete(0, tk.END)

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_button = tk.Button(root, text="Send", command=write)
    send_button.pack()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            client.close()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


class Client:
    def __init__(self):
        pass
        # print(f"Create client")

    def start(self):
        start_client()
