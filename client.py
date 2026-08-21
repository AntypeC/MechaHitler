from tkinter import *
import socket
from threading import Thread
from PIL import Image, ImageTk
import os
import pyttsx3

script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, "./img/books-that-feel-like-this-not-the-bible-v0-lefhn190v6sd1.png")
# server_path = os.path.join(script_dir, "./server.py")

# run_server = subprocess.Popen([sys.executable, server_path])

host = '127.0.0.1'
port = 5000

tts_engine = pyttsx3.init()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((host, port))
except ConnectionRefusedError:
    print("No server launched. Try again.")

def speakit(string):
    tts_engine.say(string)
    tts_engine.runAndWait()

def typeit(widget, index, string):
    widget.configure(state="normal")
    if len(string) > 0:
        widget.insert(index, string[0])
        if len(string) > 1:
            index = widget.index("%s + 1 char" % index)
            widget.after(50, typeit, widget, index, string[1:])
    widget.configure(state="disabled")

def receive_message():
    while True:
        raw = client_socket.recv(1024)
        if not raw:
            print("")
        data = raw.decode('utf-8').lower()
        print(data)
        chat_container.configure(state="normal")
        chat_container.insert(END, "MechaHitler: ")
        chat_container.configure(state="disabled")

        typeit(chat_container, "end", data+"\n")
        speakit(data)

def submit(user_entry):
    message = user_entry.get()
    entry.delete(0, END)
    message = message.lower().strip()
    client_socket.sendall(message.encode())
    chat_container.configure(state="normal")
    chat_container.insert(END, "You: "+message+"\n")
    chat_container.configure(state="disabled")

root = Tk()
root.geometry('2000x1200')
user_entry = StringVar(value="")

top_frame = Frame(root)
top_frame.pack(fill="both", expand=True)

name = Label(top_frame, text="Chatroom")
name.pack(side="top")

bottom_frame = Frame(top_frame)
bottom_frame.pack(side="bottom", fill="x")

img = Image.open(img_path).resize((600, 600))
tk_image = ImageTk.PhotoImage(img)
insert_image = Label(top_frame, image=tk_image)
insert_image.pack(side="right")

chat_container = Text(top_frame, height=25, width=120)
chat_container.configure(state="disabled")
chat_container.pack(side="left", fill="both", expand=True, padx=10, pady=(5, 5))

entry = Entry(bottom_frame, textvariable=user_entry)
entry.pack(side=LEFT, fill="x", expand=True, padx=10, pady=(10, 5))

send_button = Button(bottom_frame, command=lambda: submit(user_entry), text="Send", width=10)
send_button.pack(side=RIGHT, padx=10, pady=(10, 5))

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