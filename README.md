# ChatAppP2P
Computer Network Project - Chat Application Using P2P Model

I'm using Tkinter and Websocket in Python for this application.

You should change the database in server file to be able to use it.

1.Change the admin database in all of my files, run my SQL file
Here:
![image](https://user-images.githubusercontent.com/62462668/219930347-0006ef6f-e7a8-4ede-862d-cca9e7eecc49.png)

2. Run server.py 

and let the server open, don't turn it off

3. Run testasyncserver.py
This is my client file, though it could be a server file too cause I use a P2P Hybrid model.

Simple Explanation:
Peers Sign In/SignUp/AddFriend with the support of server.
Peers can find each other by the help of server but make a connection to chat with each other directly (P2P), which means the message go directly between 2 peers, not
going through server


Overview:


My Sign In Interface:
![image](https://user-images.githubusercontent.com/62462668/219929373-a342c3ff-15cb-4d49-869d-3f64829aa381.png)

My Sign Up Interface:
![image](https://user-images.githubusercontent.com/62462668/219930027-e0c95d27-7e58-4e19-b83b-fb1c2ceb6bea.png)

