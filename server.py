import socket
import mysql.connector
import threading
import sys

#   Functions and constants for message handling

sys.path.append('..')

from mutual.messageModule import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()

#   SQL setup

#   File containing login credentials

import secret.credentials as cred

db = mysql.connector.connect(
    host=cred.host,
    port=cred.port,
    user=cred.user,
    passwd=cred.passwd,
    database=cred.database
)

my_cursor = db.cursor()


#   Main data-structure
#   online_users{
#       client_id : {   socket : ...
#                       username : ... }
#   }

#   Temporary data-structure where we bind usernames to client id's
#   users = {username : user_id}

online_users = {}

users = {}

#   Functions

def recieve():
    #   identifier for client
    client_id = 0

    while True:
        socket, address = server.accept()
        print("NEW CLIENT CONNECTED!")

        #   Creating entry in main data-structure

        online_users[client_id] = {"socket" : socket}

        client_thread = threading.Thread(target=connected, args=(client_id,))
        client_thread.daemon = True
        client_thread.start()

        client_id += 1


def connected(client_id):
    while True:
        create = "CREATE_ACCOUNT"
        login = "LOG_IN"
        quit = "QUIT"
        
        message, flag = getMessage(online_users[client_id]["socket"])

        if message == create:
            createAccount(client_id)
        elif message == login:
            logIn(client_id)
        elif message == quit:
            sys.exit(0)

        #   Input control exists at client-side


def createAccount(client_id):

    username, flag = getMessage(online_users[client_id]["socket"])
    password, flag = getMessage(online_users[client_id]["socket"])

    try:
        my_cursor.execute(f"INSERT INTO user_accounts VALUES('{username}', '{password}', False)")
        sendMessage(online_users[client_id]["socket"], "account_created")
        db.commit()

    except Exception as e:
        sendMessage(online_users[client_id]["socket"], str(e))



def logIn(client_id):
    username, flag = getMessage(online_users[client_id]["socket"])
    password, flag = getMessage(online_users[client_id]["socket"])

    print(username)
    print(password)

    try: 
        my_cursor.execute(f"SELECT username, passw FROM user_accounts WHERE username='{username}'")
        print("TRY SUCCESS")

    except Exception as e:
        #   If username is not in database 
        sendMessage(online_users[client_id]["socket"], str(e))
        print("IN EXCEPTION")
        return

    results = my_cursor.fetchall()

    if not results:
        failedLogin(client_id)

    else:
        db_username = results[0][0]
        db_password = results[0][1]

        if username == db_username and password == db_password:
            #   Bind username to a client_id
            online_users[client_id]["username"] = username
            users[username] = client_id

            print(username)
            print(online_users[client_id]["username"])
            if(online_users[client_id]["username"] == username):
                print("True")
            else:
                print("False")

            loggedIn(client_id)

        elif username == db_username and not password == db_password:
            failedLogin(client_id)
    

def failedLogin(client_id):
    #   Send message to client

    sendMessage(online_users[client_id]["socket"], "fail")



def loggedIn(client_id):
    print("Client successfully logged in")

    #   Send message to client
    sendMessage(online_users[client_id]["socket"], "success")

    chatApp(client_id)


def controlThread():
    while True:
        sysMessage = input()

        #   Shut down server
        if sysMessage.lower() == "quit":
            cleanUp()
            
def cleanUp():

    server.close()
    sys.exit(0)


#   Chat application
    
def chatApp(client_id):
    #   Update online status for user
    print(online_users[client_id]['username'])

    #   This line occasionally produces problems, I'm assuming this issue comes from previous instances of program
    #   not closing resources correctly and still accessing database

    my_cursor.execute(f"UPDATE user_accounts SET online=True WHERE username='{online_users[client_id]['username']}'")

    while True:
        send = "SEND_MESSAGE"
        search = "VIEW_USERS"
        quit = "QUIT"
        message, sender = getMessage(online_users[client_id]["socket"])
        
        if message == send:
            sendMessageClient(client_id)
        elif message == search:
            viewClients(client_id)
        elif message == quit:
            quitChat(client_id)

def sendMessageClient(client_id):
    #   Recieve message + recipient

    message, sender = getMessage(online_users[client_id]["socket"])
    recipient, sender = getMessage(online_users[client_id]["socket"])

    #   Check if recipient is online

    my_cursor.execute(f"SELECT username FROM user_accounts WHERE username='{recipient}' AND online=True")
    results = my_cursor.fetchall()

    if results:
        #   Recipient exists and is online, flag: 1

        #   Method to extract socket of recipient
        username_rec = results[0][0]
        recieving_id = users[username_rec]
        recievingClient = online_users[recieving_id]["socket"]


        #   Send message with sender information
        sendMessage(recievingClient, message, online_users[client_id]["username"])

        #   Return status
        sendMessage(online_users[client_id]["socket"], str(1))

    else:
        #   Check if recipient exists
        my_cursor.execute(f"SELECT username FROM user_accounts WHERE username='{recipient}'")
        results = my_cursor.fetchall()

        if results:
            #   Recipient exists but is not online, flag: 2
            #   Return status
            sendMessage(online_users[client_id]["socket"], str(2))
        else:
            #   Recipient does not exist, flag: 3
            #   Return status
            sendMessage(online_users[client_id]["socket"], str(3))



def viewClients(client_id):
    my_cursor.execute("SELECT username FROM user_accounts WHERE online=True")
    results = my_cursor.fetchall()
    entry_count = 0

    #   Count number of online users to send

    for result in results:
        entry_count += 1

    #   send the count
        
    sendMessage(online_users[client_id]["socket"], str(entry_count))

    #   send the online users

    for entry in results:
        sendMessage(online_users[client_id]["socket"], entry[0])

    #   corresponding operations for offline users

    my_cursor.execute("SELECT username FROM user_accounts WHERE online=False")
    results = my_cursor.fetchall()
    entry_count = 0

    for result in results:
        entry_count += 1
        
    sendMessage(online_users[client_id]["socket"], str(entry_count))

    for entry in results:
        sendMessage(online_users[client_id]["socket"], entry[0])


def quitChat(client):
    pass

if __name__ == '__main__': 

    #   Start of program
    listening_thread = threading.Thread(target=recieve)
    listening_thread.daemon = True
    listening_thread.start()

    #   Allow user at server-end control
    controlThread()
