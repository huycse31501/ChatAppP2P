import tkinter as tk
import tkinter.ttk as ttk
import pickle
import socket
from tkinter import messagebox


class createPayload:
    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type


class AddFriendWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.transient(master)
        self.geometry("250x100")
        self.title("Add a Friend")

        main_frame = ttk.Frame(self)

        username_label = ttk.Label(main_frame, text="Username")
        self.username_entry = ttk.Entry(main_frame)

        add_button = ttk.Button(main_frame, text="Add",
                                command=self.add_friend)

        username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.username_entry.focus_force()

        add_button.grid(row=1, column=0, columnspan=2)

        for i in range(2):
            tk.Grid.columnconfigure(main_frame, i, weight=1)
            tk.Grid.rowconfigure(main_frame, i, weight=1)

        main_frame.pack(fill=tk.BOTH, expand=1)

    def add_friend(self):
        fusername = self.username_entry.get()
        username = self.master.myusername
        if fusername:
            self.username_entry.delete(0, tk.END)
            peerfriend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peerfriend.connect(("localhost", 1))
            datasend = pickle.dumps(createPayload(
                username, fusername, "AddFriend"))
            peerfriend.send(datasend)
            datareceive = peerfriend.recv(1024).decode()
            messagebox.showinfo(title=None, message=datareceive)
            peerfriend.shutdown(socket.SHUT_WR)
            peerfriend.close()
