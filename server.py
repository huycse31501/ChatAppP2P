import mysql.connector
from mysql.connector import Error
import hashlib
import socket
import threading
from tkinter import messagebox
import pickle
from contextlib import contextmanager


@contextmanager
def socketcontext(*args, **kw):
    s = socket.socket(*args, **kw)
    try:
        yield s
    finally:
        s.close()


class createPayload:
    def __init__(self, username, password, type, port=None):
        self.username = username
        self.password = password
        self.type = type
        self.port = port

# AFINET -> IPv4 SOCKSTREAM => TCP


# peerhome = {}

def handle_connection(c):
    while True:
        try:
            datarec = client.recv(4096)
            payload = pickle.loads(datarec)
        except:
            raise Exception("Login Out, No more data sent")
        try:
            command = payload.type
            if (command == None):
                return
            elif (command == "SignUp"):
                username = payload.username
                password = payload.password
                conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                if conn.is_connected():
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                        "INSERT INTO USER (username, password,isonline) VALUES (%s, %s,%s)", (username, password, False))
                    except:
                        cursor.close()
                        conn.close()
                        m = 1/0
                    conn.commit()
                    cursor.close()
                    conn.close()
                    c.send((payload.type + "Successfully").encode())
            elif (command == "SignIn"):
                username = payload.username
                password = payload.password
                # peerhome[username] = newport
                conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                if conn.is_connected():
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT username, password, isonline FROM USER WHERE username = %s AND password = %s", (username, password))
                    infoacc = cursor.fetchall()
                    if len(infoacc) != 0:
                        if (infoacc[0][2] == 1):
                            c.send("User is already logged in".encode())
                            # peerhome[username] = 0
                            cursor2 = conn.cursor()
                            cursor2.execute(
                            "UPDATE USER SET address = %s, isonline = %s WHERE username = %s", (0, False, username))
                            conn.commit()
                            cursor.close()
                            conn.close()
                            c.close()
                            return
                    else:
                        c.send("Account is not exist".encode())
                        cursor.close()
                        conn.close()
                        return
                    c.send((payload.type + "Successfully").encode())
                    cursor.close()
                    conn.close()
            elif (command == "SignOut"):
                username = payload.username
                password = payload.password
                conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                if conn.is_connected():
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE USER SET address = %s, isonline = %s WHERE username = %s", (0, False, username))
                    conn.commit()
                    # peerhome.pop(username, None)
                    cursor.close()
                    conn.close()
                    c.send((payload.type + "Successfully").encode())
            elif (command == "AddFriend"):
                username = payload.username
                fusername = payload.password
                conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                if conn.is_connected():
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO FUSER (username,fusername) VALUES (%s,%s)", (fusername, username))
                        cursor.execute(
                            "INSERT INTO FUSER (username,fusername) VALUES (%s,%s)", (username, fusername))
                    except:
                        c.send(
                            ("Addfriend Failed or Friends already added").encode())
                        raise Exception("Handle Failed")
                    conn.commit()
                    c.send((payload.type + "Successfully").encode())
                    # if cursor.fetchall():
                    #     print(cursor.fetchall())
                    #     cursortemp = conn.cursor()
                    #     cursortemp.execute(
                    #         "SELECT username FROM FUSER WHERE username = %s", (username,))
                    #     if cursortemp.fetchall():
                    #         cursor2 = conn.cursor()
                    #         cursor3 = conn.cursor()
                    #         cursor2.execute("INSERT INTO FUSER (username,fusername) VALUES (%s,%s)", (username,fusername))
                    #         cursor3.execute("INSERT INTO FUSER (username,fusername) VALUES (%s,%s)", (fusername,username))
                    #         cursor2.close()
                    #         cursor3.close()
                    #         cursortemp.close()
                    #         conn.commit()
                    #     else:
                    #         cursor2 = conn.cursor()
                    #         cursor2.execute("INSERT INTO FUSER (username,fusername) VALUES (%s,%s)", (username,fusername))
                    #         conn.commit()
                    #         cursor2.close()
                    conn.close()
            elif (command == "GetPort"):
                fusername = payload.username
                conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                if conn.is_connected():
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "SELECT ADDRESS FROM USER WHERE USERNAME = %s", (fusername,))
                        port = cursor.fetchall()[0][0]
                    except:
                        c.send(
                            ("ConnectFailed").encode())
                        raise Exception("Handle Failed")
                    conn.commit()
                    cursor.close()
                    conn.close()
                    c.send(port.encode())
            elif (command == "GetFriendList"):
                username = payload.username
                conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                if conn.is_connected():
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                             "SELECT fusername FROM FUSER WHERE username = %s", (username,))
                        port = cursor.fetchall()
                        port = pickle.dumps(port)
                        c.send(port)
                    except:
                        c.send(pickle.dumps(
                            ("ConnectFailed")))
                        raise Exception("Handle Failed")
                    conn.close()
                    cursor.close()
            # elif (command == "PortAssign"):
            #     username = payload.username
            #     c.send(str(peerhome[username]).encode())
            elif (command == "isonl"):
                username = payload.username
                conn = mysql.connector.connect(
                    host='localhost', password='huy123', user='root', database="chatapp")
                if conn.is_connected():
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                             "SELECT isonline FROM USER WHERE username = %s", (username,))
                        isonl = cursor.fetchall()[0][0]
                    except:
                        c.send(
                            ("ConnectFailed").encode())
                        raise Exception("Handle Failed")
                    conn.close()
                    cursor.close()
                    c.send(str(isonl).encode())
        except:
            c.send((payload.type + "Failed").encode())
            raise Exception("Handle Failed")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1))  # port signin singup
s.listen()

while True:
    client, addr = s.accept()
    t1 = threading.Thread(target=handle_connection,
                          args=(client,)).start()
# try:
#             peerchat1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             peerchat1.connect(("localhost", 1))
#             infopeer = pickle.dumps(createPayload(
#                 friendname, None, "GetPort"))
#             peerchat1.send(infopeer)
#             port = peerchat1.recv(1024).decode()
#             peerchat1.shutdown(socket.SHUT_WR)
#             peerchat1.close()
#         except Error as e:
#             messagebox.showerror(title=None, message=e)