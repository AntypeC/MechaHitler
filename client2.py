from tkinter import *
import socket
from threading import Thread
import queue
import time

host = '127.0.0.1'
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((host, port))
except ConnectionRefusedError:
    print("No server launched. Try again.")

def typeit(widget, index, string):
    if len(string) > 0:
        widget.insert(index, string[0])
        if len(string) > 1:
            index = widget.index("%s + 1 char" % index)
            widget.after(50, typeit, widget, index, string[1:])

def receive_message():
    while True:
        raw = client_socket.recv(1024)
        if not raw:
            print("")
        data = raw.decode('utf-8')
        print(data)
        display.insert(END, "User 2: ")
        typeit(display, "end", data+"\n")

def submit(user_entry):
    message = user_entry.get()
    entry.delete(0, END)
    message = message.lower().strip()
    client_socket.sendall(message.encode())
    display.insert(END, "User 1: "+message+"\n")

root = Tk()
root.geometry('500x350')
user_entry = StringVar(value="")

content = Frame(root, width=150)
content.pack()
name = Label(content, text="Chatroom")
name.pack()

display = Text(content, height=15, width=50)
display.pack()

entry = Entry(content, textvariable=user_entry)
entry.pack(side=LEFT, padx=50, pady=5)

send_button = Button(content, command=lambda: submit(user_entry), text="Send", width=10)
send_button.pack(side=RIGHT, padx=50, pady=5)

loop_thread = Thread(target=receive_message, daemon=True)
loop_thread.start()

root.bind("<Return>", lambda event: submit(user_entry))

root.title("Client")
root.mainloop()

# print('Elliot\'s favourite quote is "hello"')
# print("antype", end="$")
# print(32, end="")

# name = "antype"
# age = 20
# print(name, age, "hello", 10, sep=". ", end=".\n")
# print(name + ". " + str(age))

# variable = 2.6322442
# print(f"text, {variable:%<6.4f}")

# weight = 82.4324
# print(f'the weight is: {weight:.1f}kg')

# temp = 7
# temp2 = 14
# print(f"The temperature is: {temp:2d}")
# print(f"The temperature is: {temp2:1d}")

# c1 = 'Auckland'
# c2 = 'Sydney'
# c3 = 'Toronto'
# t1 = 17.5
# t2 = 25
# t3 = 3
# print(f'The temperature in {c1:>8s} is {int(t1):4d}')
# print(f'The temperature in {c2:>8s} is {t2:>4.1f}')
# print(f'The temperature in {c3:>8s} is {t3:>4.1f}')

# value = 6 == 6 or 5 > 4
# value2 = 3 > 9 and 2 == 2
# print(not value and value or value2)