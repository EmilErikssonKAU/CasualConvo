import socket
import sys
import threading
import time
from colorama import Fore, Style

#   Functions and constants for message handling

from messageModule import *

#   Networking setup

SERVER_IP = "127.0.0.1"
SERVER_PORT = 7828

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

#   Message buffer

message_buffer = []

#   Functions

def connected():
    create = "CREATE_ACCOUNT"
    login = "LOG_IN"
    quit = "QUIT"
    
    while True:
        option = input(f"{create}, {login} or {quit}:\n")

        if option == create or option == login or option == quit:
            sendMessage(client, option)

            if option == create:
                createAccount()
            elif option == login:
                logIn()
            elif option == quit:
                quitApplication()
        else:
            print("FAULTY INPUT!")

    
def createAccount():

    username = input("USERNAME: ")
    password = input("PASSWORD: ")
    sendMessage(client, username)
    sendMessage(client, password)

    # report status
    print(waitTilPop())


def quitApplication():
    client.close()
    sys.exit(0)


def logIn():
    username = input("USERNAME: ")
    password = input("PASSWORD: ")
    sendMessage(client, username)
    sendMessage(client, password)

    message = waitTilPop()

    if message == 'success':
        chatApp()
    else:
        print("Used login credentials are incorrect")
        

#   Chat application

def chatApp():
    while True:
        send = "SEND_MESSAGE"
        view = "VIEW_USERS"
        quit = "QUIT"

        option = input(f"{send}, {view} or {quit}:\n")
        if option == send or option == view or option == quit:
            sendMessage(client, option)

            if option == send:
                sendMessageClient()
            elif option == view:
                viewClients()
            elif option == quit:
                quitChat()
            else:
                continue
            
def sendMessageClient():
    message = input("Message: ")
    sendMessage(client, message)

    recipient = input("Recieving user: ")
    sendMessage(client, recipient)

    #   Recieve status:
    #       1 -> message delivered
    #       2 -> recipient is offline
    #       3 -> recipient does not exist

    #   Status is char
    status =  waitTilPop()

    if status =='1':
        print("Message sent!")
    elif status == '2':
        print("Recipient if offline, message not sent!")
    elif status == '3':
        print("Recipient does not exist")
    else:
        print("Unknown status message")



def viewClients():
    #   Online clients

    print(f"{Fore.GREEN}Online:{Style.RESET_ALL}")

    count = int(waitTilPop())

    for x in range(count):
        user = waitTilPop()
        print(user)

    #   Offline clients
        
    print(f"{Fore.RED}Offline:{Style.RESET_ALL}")

    count = int(waitTilPop())

    for x in range(count):
        user = waitTilPop()
        print(user)

def quitChat():
    #   Temporary, needs to handle resources correctly and to communicate with server
    quitApplication()

def messageReading():
    while True:
        message, flag = getMessage(client)

        if flag:
            print(f"Incoming message: {message}")
        else:
            message_buffer.append(message)
        
def waitTilPop():
    while True:
        recieved = False
        try:
            message = message_buffer.pop(0)
            recieved = True
        except:
            time.sleep(0.01)
        if recieved:
            return message
    

listening_thread = threading.Thread(target=messageReading)
listening_thread.daemon = True
listening_thread.start()

#   Start of execution
connected()


