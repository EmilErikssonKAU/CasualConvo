import tkinter as tk
from tkinter import ttk


class client(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cryptochat client")

        #   Dropdown bar on the left
        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Option 1")
        self.dropdown = ttk.Combobox(self, textvariable=self.dropdown_var, values=["Option 1", "Option 2", "Option 3"])

        #   Top-right label
        self.label_top_right = tk.Label(self, text="Conversation with ?")
        
        #   Top-left label
        self.label_top_left = tk.Label(self, text="Logged in as ?")

        #   Text window without input
        self.text_window = tk.Text(self, width=30, height=10, state=tk.DISABLED)

        #   Smaller text window for input
        self.input_text = tk.Text(self, width=30, height=3)

        #   Send button
        self.send_button = tk.Button(self, text="Send")
        self.send_button.bind('<Button-1>', self.send_btn_clicked)

        #   Notification area
        self.notification_board = tk.Label(self, text="Notification!", fg="red")

        #   Gridlayout
        self.dropdown.grid(row=1, column=0, rowspan=2, padx=10, pady=5, sticky="N")
        self.label_top_right.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
        self.label_top_left.grid(row=0, column=0, padx=10, pady=5)
        self.text_window.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        self.input_text.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
        self.send_button.grid(row=3, column=2, padx=10, pady=5, sticky="E")
        self.notification_board.grid(row=2, rowspan=2 ,column=0, padx=10, pady=5)

        #   Run the main-loop
        self.mainloop()

    def send_btn_clicked(self, event):
        pass


if __name__ == "__main__":
    client()

