import socket
import mysql.connector
import threading
import sys

#   Functions and constants for message handling

sys.path.append('..')

from mutual.messageModule import *


#   Networking setup

HOST = "127.0.0.1"
PORT = 7823

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
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

#   Lists of resources

clients = []

#   Mapping of usernames to sockets
#   'username' : socket

online_users = {}

#   Functions

def recieve():
    while True:
        client, address = server.accept()
        clients.append(client)
        print("NEW CLIENT CONNECTED!")

        client_thread = threading.Thread(target=connected, args=(client,))
        client_thread.daemon = True
        client_thread.start()


def connected(client):
    while True:
        create = "CREATE_ACCOUNT"
        login = "LOG_IN"
        quit = "QUIT"
        
        message, flag = getMessage(client)

        if message == create:
            createAccount(client)
        elif message == login:
            logIn(client)
        elif message == quit:
            clients.remove[client]
            sys.exit(0)

        #   Input control exists at client-side


def createAccount(client):

    username, flag = getMessage(client)
    password, flag = getMessage(client)

    try:
        my_cursor.execute(f"INSERT INTO user_accounts VALUES('{username}', '{password}', False)")
        sendMessage(client, "account_created")
        db.commit()

    except Exception as e:
        sendMessage(client, str(e))



def logIn(client):
    username, flag = getMessage(client)
    password, flag = getMessage(client)

    try: 
        my_cursor.execute(f"SELECT username, passw FROM user_accounts WHERE username='{username}'")

    except Exception as e:
        #   If username is not in database 
        sendMessage(client, str(e))
        return

    results = my_cursor.fetchall()

    if not results:
        failedLogin(client)

    else:
        db_username = results[0][0]
        db_password = results[0][1]

        if username == db_username and password == db_password:
            loggedIn(client, username)
        elif username == db_username and not password == db_password:
            failedLogin(client)
    

def failedLogin(client):
    #   Send message to client

    sendMessage(client, "fail")



def loggedIn(client, username):
    print("Client successfully logged in")
    #   Send message to client

    sendMessage(client, "success")

    #   Add username:socket to online_users

    online_users[username] = client
    chatApp(client, username)


def controlThread():
    while True:
        sysMessage = input()

        #   Shut down server
        if sysMessage.lower() == "quit":
            cleanUp()
            
def cleanUp():

    try:
        for client in clients:
                client.close()
    except:
        #   Will result in unclosed client sockets, unsure if a problem
        pass

    server.close()
    sys.exit(0)


#   Chat application
    
def chatApp(client, username):
    #   Update online status for user
    my_cursor.execute(f"UPDATE user_accounts SET online=True WHERE username='{username}'")

    while True:
        send = "SEND_MESSAGE"
        search = "VIEW_USERS"
        quit = "QUIT"
        message, flag = getMessage(client)
        
        if message == send:
            sendMessageClient(client)
        elif message == search:
            viewClients(client)
        elif message == quit:
            quitChat(client)

def sendMessageClient(client):
    #   Recieve message + recipient

    message, flag = getMessage(client)
    recipient, flag = getMessage(client)

    #   Check if recipient is online

    my_cursor.execute(f"SELECT username FROM user_accounts WHERE username='{recipient}' AND online=True")
    results = my_cursor.fetchall()

    if results:
        #   Recipient exists and is online, flag: 1
        username = results[0][0]
        recievingClient = online_users[username]

        #   Send message
        sendMessage(recievingClient, message, True)

        #   Return status
        sendMessage(client, str(1))

    else:
        #   Check if recipient exists
        my_cursor.execute(f"SELECT username FROM user_accounts WHERE username='{recipient}'")
        results = my_cursor.fetchall()

        if results:
            #   Recipient exists but is not online, flag: 2
            #   Return status
            sendMessage(client, str(2))
        else:
            #   Recipient does not exist, flag: 3
            #   Return status
            sendMessage(client, str(3))



def viewClients(client):
    my_cursor.execute("SELECT username FROM user_accounts WHERE online=True")
    results = my_cursor.fetchall()
    entry_count = 0

    #   Count number of online users to send

    for result in results:
        entry_count += 1

    #   send the count
        
    sendMessage(client, str(entry_count))

    #   send the online users

    for entry in results:
        sendMessage(client, entry[0])

    #   corresponding operations for offline users

    my_cursor.execute("SELECT username FROM user_accounts WHERE online=False")
    results = my_cursor.fetchall()
    entry_count = 0

    for result in results:
        entry_count += 1
        
    sendMessage(client, str(entry_count))

    for entry in results:
        sendMessage(client, entry[0])


def quitChat(client):
    pass

if __name__ == '__main__': 

    #   Start of program
    listening_thread = threading.Thread(target=recieve)
    listening_thread.daemon = True
    listening_thread.start()

    #   Allow user at server-end control
    controlThread()
