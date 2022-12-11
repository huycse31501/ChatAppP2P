import os

import tkinter as tk
import tkinter.ttk as ttk
import threading
from smilieselect import SmilieSelect
import pickle
import socket
from tkinter.filedialog import askopenfilename
SEPERATOR = "<SEPERATOR>"


class createPayload:
    def __init__(self, username, password, type, port=None):
        self.username = username
        self.password = password
        self.type = type
        self.port = port


class ChatWindow(tk.Toplevel):
    def __init__(self, master, friend_name, friend_avatar, friendport, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.title(friend_name)
        self.geometry('800x640')
        self.minsize(800, 640)
        self.friendname = friend_name
        self.friendport = int(friendport)
        # self.chatserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.chatserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.chatserver.bind(("localhost", int(myport)*50))  # port signin singup
        # self.chatserver.listen()
        # self.t1 = threading.Thread(target = self.listener,
        #                                         args=(self.chatserver,)).start()

        self.right_frame = tk.Frame(self)
        self.left_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self.left_frame)
        self.messages_area = tk.Text(
            self.left_frame, bg="white", fg="black", wrap=tk.WORD, width=30)
        self.scrollbar = ttk.Scrollbar(
            self.left_frame, orient='vertical', command=self.messages_area.yview)
        self.messages_area.configure(yscrollcommand=self.scrollbar.set)

        self.text_area = tk.Text(
            self.bottom_frame, bg="white", fg="black", height=3, width=30)
        self.text_area.smilies = []
        self.send_button = ttk.Button(
            self.bottom_frame, text="Send", command=self.send_message, style="send.TButton")
        self.send_file = ttk.Button(
            self.bottom_frame, text="File", command=self.send_file, style="send.TButton")

        self.smilies_image = tk.PhotoImage(
            file="smilies/mikulka-smile-cool.png")
        self.smilie_button = ttk.Button(
            self.bottom_frame, image=self.smilies_image, command=self.smilie_chooser, style="smilie.TButton")

        self.profile_picture = tk.PhotoImage(file="images/avatar.png")
        self.friend_profile_picture = tk.PhotoImage(file=friend_avatar)

        self.profile_picture_area = tk.Label(
            self.right_frame, image=self.profile_picture, relief=tk.RIDGE)
        self.friend_profile_picture_area = tk.Label(
            self.right_frame, image=self.friend_profile_picture, relief=tk.RIDGE)

        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.messages_area.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.messages_area.configure(state='disabled')

        self.right_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.profile_picture_area.pack(side=tk.BOTTOM)
        self.friend_profile_picture_area.pack(side=tk.TOP)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.smilie_button.pack(side=tk.LEFT, pady=5)
        self.text_area.pack(side=tk.LEFT, fill=tk.X, expand=1, pady=5)
        self.send_button.pack(side=tk.RIGHT, pady=5)
        self.send_file.pack(side=tk.RIGHT, pady=5)

        self.configure_styles()
        self.bind_events()

    def bind_events(self):
        self.bind("<Return>", self.send_message)
        self.text_area.bind("<Return>", self.send_message)

        self.text_area.bind('<Control-s>', self.smilie_chooser)

    def send_message(self):
        message = self.text_area.get(1.0, tk.END)
        infosend = pickle.dumps(createPayload(
            self.friendname, message, "sent", self.friendport))
        peerchat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peerchat.connect(("localhost", self.friendport))
        peerchat.send(infosend)
        peerchat.recv(1024).decode()
        if message.strip() or len(self.text_area.smilies):
            message = "Me: " + message
            self.messages_area.configure(state='normal')
            self.messages_area.insert(tk.END, message)

            if len(self.text_area.smilies):
                last_line_no = self.messages_area.index(tk.END)
                last_line_no = str(last_line_no).split('.')[0]
                last_line_no = str(int(last_line_no) - 2)

                for index, file in self.text_area.smilies:
                    char_index = str(index).split('.')[1]
                    char_index = str(int(char_index) + 4)
                    smilile_index = last_line_no + '.' + char_index
                    self.messages_area.image_create(smilile_index, image=file)

                self.text_area.smilies = []

            self.messages_area.configure(state='disabled')

            self.text_area.delete(1.0, tk.END)

        return "break"

    def send_file(self):
        filename = askopenfilename()
        def filethread(filename):
            filesize = os.path.getsize(filename)
            infofile = createPayload(
                self.master.myusername, f"{filename}{SEPERATOR}{filesize}", "file")
            peersent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peersent.connect(("localhost", self.friendport))
            peersent.send(pickle.dumps(infofile))
            peersent.recv(1024).decode()
            with open(filename, "rb") as f:
                while True:
                    bytes = f.read(4096)
                    if not bytes:
                        break
                    peersent.sendall(bytes)
            peersent.shutdown(socket.SHUT_WR)
            peersent.close()
            self.receive_message("System", filename + " is sent \n")
            return
        t1 = threading.Thread(target=filethread,args=(filename,)).start()

    def smilie_chooser(self, event=None):
        SmilieSelect(self)

    def add_smilie(self, smilie):
        smilie_index = self.text_area.index(
            self.text_area.image_create(tk.END, image=smilie))
        self.text_area.smilies.append((smilie_index, smilie))

    def receive_message(self, author, message):

        message = message

        if message.strip() or len(self.text_area.smilies):
            message = str(author) + ": " + message
            self.messages_area.configure(state='normal')
            self.messages_area.insert(tk.END, message)

            if len(self.text_area.smilies):
                last_line_no = self.messages_area.index(tk.END)
                last_line_no = str(last_line_no).split('.')[0]
                last_line_no = str(int(last_line_no) - 2)

                for index, file in self.text_area.smilies:
                    char_index = str(index).split('.')[1]
                    char_index = str(int(char_index) + 4)
                    smilile_index = last_line_no + '.' + char_index
                    self.messages_area.image_create(smilile_index, image=file)

                self.text_area.smilies = []

            self.messages_area.configure(state='disabled')

        return "break"

    def configure_styles(self):
        style = ttk.Style()
        style.configure("send.TButton", background='#dddddd',
                        foreground="black", padding=16)

    def listener(self, myserver):
        def handle_connection(peer):
            while True:
                try:
                    datarec = peer.recv(4096)
                    payload = pickle.loads(datarec)
                except:
                    raise Exception("Sent Complete")
                command = payload.type
                if (command == "sent"):
                    self.receive_message(payload.username, payload.password)
                    peer.send("Accquire Text".encode())
        while True:
            peer, addr = myserver.accept()
            t1 = threading.Thread(target=handle_connection,
                                  args=(peer,)).start()

    # def listencon(self):
    #     def handle_connection():
    #         try:
    #             datarec = peer.recv(4096)
    #             payload = pickle.loads(datarec)
    #         except:
    #             raise Exception("Login Out, No more data sent")
    #         try:
    #             command = payload.type
    #             if (command == None):
    #                 return
    #             elif (command == "sendmes"):
    #                 username = payload.username
    #                 self.receive_message(username)
    #         except:
    #             peer.send((payload.type + "Failed").encode())
    #             raise Exception("Handle Failed")
    #         finally:
    #             peer.send(("Connection Successfully").encode())
    #     while True:
    #         peer, addr = self.recon.accept()
    #         t1 = threading.Thread(target=handle_connection,
    #                         args=(peer,)).start()
