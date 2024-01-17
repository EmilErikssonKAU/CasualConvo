import tkinter as tk
import socket
import sys
import threading
import time
from colorama import Fore, Style
import app_gui as ap

#   Functions and constants for message handling

sys.path.append('..')

from mutual.messageModule import *


#   GUI

#   Classes

class client_entity:
    def __init__ (self):
        #   Server connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER_IP, SERVER_PORT))

        #   Message buffer
        self.message_buffer = []

        #   Record of user information
        self.users = {}

        #   username : { status: 
        #                conversation:            
        #              }

        #   Message reading thread
        self.messageReader = threading.Thread(target=self.messageReading)
        self.messageReader.daemon = True
        self.messageReader.start()

        #   GUI
        self.gui = login_page(self)
        

    def messageReading(self):
        while True:
            time.sleep(0.5)
            message, sender = getMessage(self.client)

            if sender == "NULL":
                self.message_buffer.append(message)
                
            else:
                #   Notify recieving user
                self.gui.notification_board.config(text=f"Message from {sender}!")

                #   Add conversation to message history
                if "conversation" not in self.users[sender]:
                    self.users[sender]["conversation"] = " "

                self.users[sender]["conversation"] += f"{sender}: {message}"

                print(f"CURRENT CONVO: {self.users[sender]['conversation']}")

                if "conversation" in self.users[sender]:
                    print("Conversation in self.users[sender]")
                else:
                    print("NOPE")
                    
        
    def waitTilPop(self):
        while True:
            recieved = False
            try:
                message = self.message_buffer.pop(0)
                recieved = True
            except:
                time.sleep(0.01)
            if recieved:
                return message


class login_page():
    def __init__(self, client_entity):
        #   Back-end client
        self.backend = client_entity

        #   Top-level tk widget
        self.root = tk.Tk()

        #   root setup
        self.root.title("Cryptochat")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        #   Welcome label
        self.welcome_label = tk.Label(self.root, text="Login", font=("Arial", 12))

        #   Username && password boxes
        self.user_entry = tk.Entry(self.root)
        self.passw_entry = tk.Entry(self.root, show="*")  

        #   Username && password labels
        self.user_label = tk.Label(self.root, text="Username: ", font=("Arial", 12))
        self.passw_label = tk.Label(self.root, text="Password: ", font=("Arial", 12))

        #   Login button
        self.login_btn = tk.Button(self.root, text="Log in")
        self.login_btn.bind('<Button-1>', self.on_login_button_click)

        #   Create account label
        self.create_acc_label_1 = tk.Label(self.root, text="Don't have an account?", font=("Arial, 10"))
        
        self.create_acc_label_2 = tk.Label(self.root, text="Create one", font=("Arial, 10"), fg="blue")
        self.create_acc_label_2.bind('<Button-1>', self.switch_to_create_account_click)

        #   Grid layout
        self.welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nswe")
        self.user_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.passw_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.user_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.passw_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.login_btn.grid(row=3, column=1, padx=10, pady=5, sticky="e")
        self.create_acc_label_1.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.create_acc_label_2.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        #   Main-loop
        self.root.mainloop()

    def on_login_button_click(self, event):
        username = self.user_entry.get()
        password = self.passw_entry.get()
        
        sendMessage(self.backend.client, "LOG_IN")
        sendMessage(self.backend.client, username)
        sendMessage(self.backend.client,password)

        message = self.backend.waitTilPop()             #   Here the program freezes

        

        if message == 'success':
            #   This is where we start the GUI app
            self.root.destroy()
            self.backend.username = username
            
            ap.mainApp(self.backend)

        else:
            
            self.user_entry.configure(bg="red")
            self.passw_entry.configure(bg="red")
        

    def switch_to_create_account_click(self, event):
        #   Destroy this window
        self.root.destroy()

        #   Create a create-account window
        create_account_page(self.backend)



class create_account_page():
    def __init__(self, backend):
        #   Top-level tk widget
        self.root = tk.Tk()

        #   Add backend
        self.backend = backend

        #   root setup
        self.root.title("Cryptochat")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        #   Welcome label
        self.welcome_label = tk.Label(self.root, text="Account creation", font=("Arial", 12))

        #   Username && password boxes
        self.user_entry = tk.Entry(self.root)
        self.passw_entry = tk.Entry(self.root, show="*")  

        #   Username && password labels
        self.user_label = tk.Label(self.root, text="New Username: ", font=("Arial", 12))
        self.passw_label = tk.Label(self.root, text="New Password: ", font=("Arial", 12))

        #   Login button
        self.create_acc_btn = tk.Button(self.root, text="Create account")
        self.create_acc_btn.bind('<Button-1>', self.on_create_account_button_click)

        #   Create account label
        self.log_in_acc_label_1 = tk.Label(self.root, text="Already have an account?", font=("Arial, 10"))
        
        self.log_in_acc_label_2 = tk.Label(self.root, text="Log in", font=("Arial, 10"), fg="blue")
        self.log_in_acc_label_2.bind('<Button-1>', self.switch_to_login_click)

        #   Grid layout
        self.welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nswe")
        self.user_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.passw_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.user_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.passw_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.create_acc_btn.grid(row=3, column=1, padx=10, pady=5, sticky="e")
        self.log_in_acc_label_1.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.log_in_acc_label_2.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        #   Main-loop
        self.root.mainloop()

    def on_create_account_button_click(self, event):
        username = self.user_entry.get()
        password = self.passw_entry.get()

        sendMessage(self.backend.client, "CREATE_ACCOUNT")
        sendMessage(self.backend.client, username)
        sendMessage(self.backend.client, password)

        message = self.backend.waitTilPop()

        if message == "account_created":
            self.user_entry.configure(bg = "green")
            self.passw_entry.configure(bg = "green")
        
        else:
            self.user_entry.configure(bg = "red")
            self.passw_entry.configure(bg = "red")

    
    def switch_to_login_click(self, event):
        #   Destroy this window
        self.root.destroy()

        #   Create a login window
        login_page(self.backend)


        
if __name__ == '__main__':
    client_entity()