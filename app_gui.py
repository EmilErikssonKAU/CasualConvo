import tkinter as tk
from tkinter import ttk
import threading
import time
from mutual.messageModule import *
import login_gui as lg


class mainApp(tk.Tk):
    def __init__(self, backend):
        super().__init__()
        #   Client configuration
        self.backend = backend

        #   Assign backends gui component
        self.backend.gui = self

        #   Current target for conversation
        self.convo_target = 0

        #   Window settings
        self.title("Cryptochat client")

        #   Frame for listbox + scrollbar
        self.lb_frame = tk.Frame(self)

        #   ListBox
        self.listbox = tk.Listbox(self.lb_frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)

        #   Listbox functio-binding
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        #   Scrollbar
        self.lb_scroll = tk.Scrollbar(self.lb_frame, command=self.listbox.yview)
        self.lb_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.lb_scroll.set)
        

        #   Top-right label
        self.label_top_right = tk.Label(self, text=f"Logged in as {self.backend.username}")
        
        #   Top-left label
        self.label_top_right = tk.Label(self, text=f"Talking with ?")

        #   Text window without input
        self.text_window = tk.Text(self, width=30, height=10)

        #   Smaller text window for input
        self.input_text = tk.Text(self, width=30, height=3)

        #   Send button
        self.send_button = tk.Button(self, text="Send")
        self.send_button.bind('<Button-1>', self.send_btn_clicked)

        #   Notification area
        self.notification_board = tk.Label(self, text="Notification!", fg="red")

        #   Gridlayout
        self.lb_frame.grid(row=1, column=0, rowspan=2, padx=10, pady=5, sticky="N")
        self.label_top_right.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
        self.text_window.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        self.input_text.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
        self.send_button.grid(row=3, column=2, padx=10, pady=5, sticky="E")
        self.notification_board.grid(row=2, rowspan=2 ,column=0, padx=10, pady=5)

        #   Update contents of scrollbar
        self.th_scrollbar = threading.Thread(target=self.updateScrollbar)
        self.th_scrollbar.daemon = True
        self.th_scrollbar.start()

        #   Update contents of text window
        self.th_textwin = threading.Thread(target=self.updateTextWindow)
        self.th_textwin.daemon = True
        self.th_textwin.start()

        #   Welcome message
        self.text_window.insert("end", "See conversations here!")

        #   Run the main-loop
        self.mainloop()

    def send_btn_clicked(self, event):
        #   Get message from input window
        message_to_send = self.input_text.get("1.0",tk.END)

        #   Clear the input window
        self.input_text.delete("1.0", tk.END)

        #   Send the message-request to the server
        sendMessage(self.backend.client, "SEND_MESSAGE")

        #   Send the message and recipient
        sendMessage(self.backend.client, message_to_send)
        sendMessage(self.backend.client, self.convo_target)
        
    def updateTextWindow(self): 
        while True:
            #   User has selected another user
            time.sleep(0.5)
            
            if self.convo_target == 0:
                continue

            #   Clear previous text
            self.text_window.delete(1.0, "end")

            try:
                #   Add new text
                self.text_window.insert("end", self.backend.users[self.convo_target]["conversation"])
                #print(self.backend.users[self.convo_target]["conversation"])
            except:
                print(f"ERROR DISPLAYING MESSAGE FROM {self.convo_target}")



    def updateScrollbar(self):
        while True:
            #   Sleep for a second
            time.sleep(1)

            #   Send request to server
            sendMessage(self.backend.client, "VIEW_USERS")

            #   Get number of online users
            online_range = int(self.backend.waitTilPop())

            print(online_range)

            for i in range(online_range):
                user = self.backend.waitTilPop()
                print(user)

                if user not in self.backend.users:
                    print("user not in self.backend.users:(online)")
                    user_dict = {}
                    self.backend.users[user] = user_dict

                self.backend.users[user]["status"] = "online"

            #   Get number of offline users
            offline_range = int(self.backend.waitTilPop())
            print(offline_range)

            for i in range(offline_range):
                user = self.backend.waitTilPop()
                print(user)

                if user not in self.backend.users:
                    print("user not in self.backend.users:(offline)")
                    user_dict = {}
                    self.backend.users[user] = user_dict

                self.backend.users[user]["status"] = "offline"

            #   Need entry count for itemconfig
            lap = 0

            for key in sorted(self.backend.users):
                if(self.backend.users[key]["status"] == "online"):
                    color = "green"
                if(self.backend.users[key]["status"] == "offline"):
                    color = "red"

                #   Add name to listbox
                if key not in self.listbox.get(0, tk.END):
                    self.listbox.insert(tk.END, key)
                self.listbox.itemconfig(lap, {'bg': color})
                lap += 1

    def on_select(self, event):
        #   Get the selected username
        selected_item = self.listbox.get(self.listbox.curselection())
        self.label_top_right.config(text=f"Conversation with {selected_item}")

        #   Current target for conversation
        self.convo_target = selected_item
        



if __name__ == "__main__":
    mainApp()

