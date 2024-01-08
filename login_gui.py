import tkinter as tk

class login_page():
    def __init__(self):
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

        

    def switch_to_create_account_click(self, event):
        #   Destroy this window
        self.root.destroy()

        #   Create a create-account window
        create_account_page()



class create_account_page():
    def __init__(self):
        super().__init__()
        #   Top-level tk widget
        self.root = tk.Tk()

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
        pass

    def switch_to_login_click(self, event):
        #   Destroy this window
        self.root.destroy()

        #   Create a login window
        login_page()

if __name__ == '__main__':
    login_page()