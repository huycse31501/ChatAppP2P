from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import ast
import re
import tkinter as tk
import socket
import tkinter.ttk as ttk
from chatwindow import ChatWindow
import os
from smilieselect import SmilieSelect
import tkinter.ttk as ttk
from friendslist import *
import pickle


class createPayload:
    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type


class windowroot(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (SignIn, SignUp):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(SignIn)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.title("Sign Up")
        controller.geometry("925x500")
        controller.configure(bg="#fff")
        controller.resizable(False, False)

        def signup():
            username = user.get()
            password = passw.get()
            if (len(username) == 0 or len(password) == 0):
                messagebox.showinfo(title=None, message="No empty field")
            elif ((username != "Username" and password != "Password")):
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect(("localhost", 1))
                    datasend = pickle.dumps(
                        createPayload(username, password, "SignUp"))
                    client.send(datasend)
                    datareceive = client.recv(1024).decode()
                    messagebox.showinfo(title=None, message=datareceive)
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                except Error as e:
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    messagebox.showinfo(title=None, message=e)
            else:
                messagebox.showinfo(title=None, message="No empty field")
        self.img = PhotoImage(file='hcmutlogo.png')
        Label(self, image=self.img, bg='white').place(x=50, y=90)

        frame = Frame(self, width=350, height=350, bg="white")
        frame.place(x=480, y=50)

        hello = Label(frame, text='Sign Up', fg='#000', bg='white',
                      font=('Microsoft YaHei UI Light', 23, 'bold'))
        hello.place(x=100, y=5)

        def submission(e):
            user.delete(0, 'end')

        def onout(e):
            name = user.get()
            if name == '':
                user.insert(0, 'Username')
        user = Entry(frame, width=25, fg='#000', border=0, bg="white",
                     font=('Microsoft YaHei UI Light', 11))
        user.place(x=30, y=80)
        user.insert(0, 'Username')
        user.bind('<FocusIn>', submission)
        user.bind('<FocusOut>', onout)

        Frame(frame, width=300, height=2, bg='black').place(x=25, y=107)

        def submission(e):
            passw.delete(0, 'end')
            passw.config(show='*')

        def onout(e):
            name = passw.get()
            if name == '':
                passw.config(show='')
                passw.insert(0, 'Password')

        passw = Entry(frame, width=25, fg='#000', border=0, bg="white",
                      font=('Microsoft YaHei UI Light', 11))
        passw.place(x=30, y=150)
        passw.insert(0, 'Password')
        passw.bind('<FocusIn>', submission)
        passw.bind('<FocusOut>', onout)
        Frame(frame, width=300, height=2, bg='black').place(x=25, y=177)

        ####

        def submission(e):
            cpassw.delete(0, 'end')
            cpassw.config(show='*')

        def onout(e):
            name = cpassw.get()
            if name == '':
                cpassw.config(show='')
                cpassw.insert(0, 'Confirm Password')

        cpassw = Entry(frame, width=25, fg='#000', border=0, bg="white",
                       font=('Microsoft YaHei UI Light', 11))
        cpassw.place(x=30, y=220)
        cpassw.insert(0, 'Confirm Password')
        cpassw.bind('<FocusIn>', submission)
        cpassw.bind('<FocusOut>', onout)
        Frame(frame, width=300, height=2, bg='black').place(x=25, y=247)

        ######
        Button(frame, width=39, pady=7, text='Submit', bg='#57a1f8',
               fg='white', border=0, command=signup).place(x=35, y=280)
        label = Label(frame, text="Already have an account -> ", fg='black',
                      bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=90, y=320)

        sign_in = Button(frame, width=6, text='Sign In', border=0,
                         bg='white', cursor='hand2', fg='#57a1f8', command=lambda: controller.show_frame(SignIn))
        sign_in.place(x=245, y=320)


SEPERATOR = "<SEPERATOR>"


class SignIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.title("Sign In")
        controller.geometry("925x500")
        controller.configure(bg="#fff")
        controller.resizable(False, False)

        def login():
            username = user.get()
            password = passw.get()
            if (len(username) == 0 or len(password) == 0):
                messagebox.showinfo(title=None, message="No empty field")
            elif ((username != "Username" and password != "Password")):
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect(("localhost", 1))
                    datasend = pickle.dumps(
                        createPayload(username, password, "SignIn"))
                    client.send(datasend)
                    datareceive = client.recv(1024).decode()
                    messagebox.showinfo(title=None, message=datareceive)
                    if (datareceive == "SignInSuccessfully"):
                        myport = 5
                        test = 0
                        myserver = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
                        while test == 0:
                            try:
                                myserver.bind(("localhost", myport))
                                test = 1
                            except:
                                myport += 1
                        # myserver = socket.socket(
                        #     socket.AF_INET, socket.SOCK_STREAM)
                        # myserver.bind(("localhost", myport))
                        myserver.listen()
                        messagebox.showinfo(
                            title=None, message="Open port: " + str(myport))
                        conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                        if conn.is_connected():
                            cursor2 = conn.cursor()
                            cursor2.execute(
                                "UPDATE USER SET address = %s, isonline = %s WHERE username = %s", (myport, True, username))
                            conn.commit()
                            cursor2.close()
                        def closesock(client):
                            datasend = pickle.dumps(createPayload(
                                username, password, "SignOut"))
                            client.send(datasend)
                            rec = client.recv(1024).decode()
                            messagebox.showinfo(title=None, message=rec)
                            client.shutdown(socket.SHUT_RDWR)
                            client.close()
                            f.destroy()
                        def listenpeer(myserver):
                            def handle_connection(peer):
                                while True:
                                    try:
                                        datarec = peer.recv(4096)
                                        payload = pickle.loads(datarec)
                                    except:
                                        raise Exception("Sent Complete")
                                    try:
                                        command = payload.type
                                        if (command == None):
                                            a = 1/0
                                        elif (command == "Connect"):
                                            friendname = payload.username
                                            try:
                                                peerchat1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                peerchat1.connect(("localhost", 1))
                                                infopeer = pickle.dumps(createPayload(
                                                    friendname, None, "GetPort"))
                                                peerchat1.send(infopeer)
                                                port = peerchat1.recv(1024).decode()
                                                port = int(port)
                                                peerchat1.shutdown(socket.SHUT_WR)
                                                peerchat1.close()
                                                peerchat1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                                peerchat1.connect(("localhost", 1))
                                                infopeer = pickle.dumps(createPayload(
                                                    username, None, "GetPort"))
                                                peerchat1.send(infopeer)
                                                myport = peerchat1.recv(1024).decode()
                                                myport = int(myport)
                                                peerchat1.shutdown(socket.SHUT_WR)
                                                peerchat1.close()
                                            except:
                                                messagebox.showerror(
                                                    title=None, message="ConnectFailed")
                                            finally:
                                                peer.send(
                                                    ("Connection Successfully").encode())
                                                peerchat = socket.socket(
                                                    socket.AF_INET, socket.SOCK_STREAM)
                                                peerchat.connect(
                                                    ("localhost", int(port)))
                                                infopeer = pickle.dumps(createPayload(
                                                    username, int(myport), "ConnectBack"))
                                                peerchat.send(infopeer)
                                                peerchat.recv(1024).decode()
                                                peerchat.shutdown(
                                                    socket.SHUT_WR)
                                                peerchat.close()
                                                f.cwin = ChatWindow(
                                                    f, friendname, 'images/avatar.png', port)
                                        elif (command == "ConnectBack"):
                                            peer.send(
                                                ("Connection Successfully").encode())
                                            f.cwin = ChatWindow(
                                                f, payload.username, 'images/avatar.png', payload.password)
                                        elif (command == "sent"):
                                            peer.send("OK".encode())
                                            f.cwin.receive_message(
                                                payload.username, payload.password)
                                        elif (command == "file"):
                                            peer.send("OK".encode())
                                            received = payload.password
                                            filename, filesize = received.split(
                                                SEPERATOR)
                                            filename = os.path.basename(
                                                filename)
                                            filesize = int(filesize)
                                            with open(filename, "wb") as fl:
                                                while True:
                                                    bytes = peer.recv(4096)
                                                    if not bytes:
                                                        break
                                                    fl.write(bytes)
                                            f.cwin.receive_message("System", filename + " is sent successfully to you, check your folder \n")
                                            peer.close()
                                    except:
                                        peer.send(
                                            (payload.type + "Failed").encode())
                                        raise Exception("Handle Failed")
                            while True:
                                peer, addr = myserver.accept()
                                t1 = threading.Thread(target=handle_connection,
                                                      args=(peer,)).start()
                        # client.shutdown(socket.SHUT_RDWR)
                        # client.close()
                        f = FriendsList(username, client, myserver)
                        f.protocol("WM_DELETE_WINDOW",
                                   lambda: closesock(client))
                        threading.Thread(target=listenpeer,
                                         args=((myserver,))).start()
                        f.mainloop()
                except Error as e:
                    messagebox.showinfo(title=None, message=e)
            else:
                messagebox.showinfo(title=None, message="No empty field")

        self.img = PhotoImage(file='hcmutlogo.png')
        Label(self, image=self.img, bg='white').place(x=50, y=90)
        frame = Frame(self, width=350, height=350, bg="white")
        frame.place(x=480, y=50)

        hello = Label(frame, text='Log In', fg='#000', bg='white',
                      font=('Microsoft YaHei UI Light', 23, 'bold'))
        hello.place(x=100, y=5)

        # uname and pass

        def submission(e):
            user.delete(0, 'end')

        def onout(e):
            name = user.get()
            if name == '':
                user.insert(0, 'Username')

        user = Entry(frame, width=25, fg='#000', border=0, bg="white",
                     font=('Microsoft YaHei UI Light', 11))
        user.place(x=30, y=80)
        user.insert(0, 'Username')
        user.bind('<FocusIn>', submission)
        user.bind('<FocusOut>', onout)

        Frame(frame, width=300, height=2, bg='black').place(x=25, y=107)

        def submission(e):
            passw.delete(0, 'end')
            passw.config(show='*')

        def onout(e):
            name = passw.get()
            if name == '':
                passw.config(show='')
                passw.insert(0, 'Password')

        passw = Entry(frame, width=25, fg='#000', border=0, bg="white",
                      font=('Microsoft YaHei UI Light', 11))
        passw.place(x=30, y=150)
        passw.insert(0, 'Password')
        passw.bind('<FocusIn>', submission)
        passw.bind('<FocusOut>', onout)
        Frame(frame, width=300, height=2, bg='black').place(x=25, y=177)

        ####
        Button(frame, width=39, pady=7, text='Log In', bg='#57a1f8',
               fg='white', border=0, command=login).place(x=35, y=204)
        label = Label(frame, text="If you are new ->", fg='black',
                      bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=75, y=270)

        sign_up = Button(frame, width=6, text='Sign Up', border=0,
                         bg='white', cursor='hand2', fg='#57a1f8', command=lambda: controller.show_frame(SignUp))
        sign_up.place(x=180, y=270)


app = windowroot()
app.mainloop()
