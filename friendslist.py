import tkinter as tk
import tkinter.ttk as ttk
from chatwindow import *
from addfriendwindow import AddFriendWindow
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import pickle
import socket
from functools import partial


class createPayload:
    def __init__(self, username, password, type, port=None):
        self.username = username
        self.password = password
        self.type = type
        self.port = port

# def closesock(client,username,password):
#     datasend = pickle.dumps(createPayload(username, password, "SignOut"))
#     client.send(datasend)
#     rec = client.recv(1024).decode()
#     messagebox.showinfo(title = None, message = rec)
#     client.shutdown(socket.SHUT_RDWR)
#     client.close()
#     f.destroy()


class FriendsList(tk.Tk):
    def show_add_friend_window(self):
        AddFriendWindow(self)

    def __init__(self, name, mycon, myserver, **kwargs):
        super().__init__(**kwargs)

        self.title(name)
        self.geometry('700x500')
        self.myusername = name
        self.mycon = mycon
        self.myserver = myserver
        self.menu = tk.Menu(self, bg="lightgrey", fg="black", tearoff=0)

        self.friends_menu = tk.Menu(
            self.menu, fg="black", bg="lightgrey", tearoff=0)
        self.friends_menu.add_command(
            label="Add Friend", command=self.show_add_friend_window)

        self.avatar_menu = tk.Menu(
            self.menu, fg="black", bg="lightgrey", tearoff=0)
        self.avatar_menu.add_command(
            label="Reload Friend", command=self.reload_friends)
        self.menu.add_cascade(label="Friends", menu=self.friends_menu)
        self.menu.add_cascade(label="Reload", menu=self.avatar_menu)

        self.configure(menu=self.menu)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas_frame = tk.Frame(self.canvas)

        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

        self.friends_area = self.canvas.create_window(
            (0, 0), window=self.canvas_frame, anchor="nw")

        self.bind_events()
        self.load_friends()

    friendlist = []
    cwin = {}

    def bind_events(self):
        self.bind('<Configure>', self.on_frame_resized)
        self.canvas.bind('<Configure>', self.friends_width)

    def friends_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.friends_area, width=canvas_width)

    def on_frame_resized(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def reload_friends(self):
        for child in self.canvas_frame.winfo_children():
            child.pack_forget()
        self.load_friends()

    def open_chat_window(self, friendname):
        try:
            peerchat1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peerchat1.connect(("localhost", 1))
            infopeer = pickle.dumps(createPayload(
                friendname, None, "GetPort"))
            peerchat1.send(infopeer)
            port = peerchat1.recv(1024).decode()
            peerchat1.shutdown(socket.SHUT_WR)
            peerchat1.close()
        except Error as e:
            messagebox.showerror(title=None, message=e)
        finally:
            peerchat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peerchat.connect(("localhost", int(port)))
            infopeer = pickle.dumps(createPayload(
                self.myusername, None, "Connect"))
            peerchat.send(infopeer)
            peerchat.recv(1024).decode()
            peerchat.shutdown(socket.SHUT_WR)
            peerchat.close()
            # cwin = ChatWindow(self, friendname, 'images/avatar.png', port, myport)

    def load_friends(self):
        try:
            peerf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peerf.connect(("localhost", 1))
            infopeer = pickle.dumps(createPayload(
                self.myusername, None, "GetFriendList"))
            peerf.send(infopeer)
            rec = peerf.recv(4096)
            self.friendlist = pickle.loads(rec)
            peerf.shutdown(socket.SHUT_WR)
            peerf.close()
        except:
            messagebox.showerror(title=None, message="Failed to get friendlist")
        finally:
            for friends in self.friendlist:
                friend = friends[0]
                friend_frame = ttk.Frame(self.canvas_frame)

                profile_photo = tk.PhotoImage(
                    file="images/avatar.png", master=self)
                profile_photo_label = ttk.Label(
                    friend_frame, image=profile_photo)
                profile_photo_label.image = profile_photo

                friend_name = ttk.Label(friend_frame, text=friend, anchor=tk.W)
                peerfg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peerfg.connect(("localhost", 1))
                infopeer = pickle.dumps(createPayload(
                    friend, None, "isonl"))
                peerfg.send(infopeer)
                isonl = peerfg.recv(1024).decode()
                isonl = int(isonl)
                peerfg.shutdown(socket.SHUT_WR)
                peerfg.close()
                msf = partial(self.open_chat_window, friendname=friend)
                message_button = ttk.Button(
                    friend_frame, text="Chat", command=msf)
                if (isonl == 0):
                    message_button["state"] = "disabled"
                profile_photo_label.pack(side=tk.LEFT)
                friend_name.pack(side=tk.LEFT)
                message_button.pack(side=tk.RIGHT)
                friend_frame.pack(fill=tk.X, expand=1)

    def listenpeer(self):
        def handle_connection():
            try:
                datarec = peer.recv(4096)
                payload = pickle.loads(datarec)
            except:
                raise Exception("Login Out, No more data sent")
            try:
                command = payload.type
                if (command == None):
                    return
                elif (command == "GetInfo"):
                    username = payload.username
                    cwin = ChatWindow(
                        self, username, 'images/avatar.png', self.myserver, peer)
            except:
                peer.send((payload.type + "Failed").encode())
                raise Exception("Handle Failed")
            finally:
                peer.send(("Connection Successfully").encode())
        while True:
            peer, addr = self.myserver.accept()
            t1 = threading.Thread(target=handle_connection,
                                  args=(peer,)).start()
