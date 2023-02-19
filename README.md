# ChatAppP2P
Computer Network Project  - Chat Application Using P2P Model

All Function:
1. Sign Up/ Sign In (Client - Server)
2. Add Friend (Client - Server)
3. Chat (P2P)
4. Send Files (P2P)

I'm using Tkinter and Websocket in Python for this application.

You should change the database in server file to be able to use it.

Remember to CD to the directory which has my project.

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

My Friendlist Interface:
![image](https://user-images.githubusercontent.com/62462668/219931423-a48e72af-e598-4d45-94a5-0e9a291429c4.png)
(Because a2 is offline, the chat button is disabled)

When a2 is online, both can chat with each other.
![image](https://user-images.githubusercontent.com/62462668/219931471-c69e3cc4-4138-4851-ad1d-39fe1f38e740.png)

My addfriend Interface:
![image](https://user-images.githubusercontent.com/62462668/219931484-fff94e4d-386c-4fd2-8a55-2eaa675043ee.png)

If friend is not in account database, its failed
![image](https://user-images.githubusercontent.com/62462668/219931523-2ddb2773-caaa-43d8-9012-f11a29504119.png)

A little bit of demo of my simple database (when using add friends, the fuser table got updated)
you can check mysql file in this repository to see DDL files.
![image](https://user-images.githubusercontent.com/62462668/219931552-aa8dc8b9-2ea6-4c2a-9fdc-66e984cdaf63.png)

Chat Interface:
![image](https://user-images.githubusercontent.com/62462668/219931617-5195bfc1-3fb2-4581-8253-7218877310bc.png)

SendFile Interface:
![image](https://user-images.githubusercontent.com/62462668/219931633-136bf675-f4db-49ef-a5ca-d08ed6aae3e3.png)

The file is indeed get there
![image](https://user-images.githubusercontent.com/62462668/219931647-f18b6d4b-a595-468a-9911-3f3c6012e998.png)

Thank you for visiting my repository.


