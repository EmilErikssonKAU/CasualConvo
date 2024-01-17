##  CasualConvo

CasualConvo is a basic client-server chat application, where registered users are allowed to send and recieve message from other registered users. The program is programmed in Python and login-information is stored inside a mySQL database.

#   How to use

As of now, no non-local server is running the application. To run the server yourself locally you must first initialise a mySQL database and adapt the mysql.connector.connect.cursor.execute() statements to match your database. I recommend the following setup:

```CREATE DATABASE login_info;```

```USE login_info;```

```CREATE TABLE user_accounts (username VARCHAR(255) PRIMARY KEY,password VARCHAR(255),status BOOLEAN);```

To run the server, you run the file server.py, to run the client you run the file login_gui.py