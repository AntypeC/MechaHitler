from tkinter import *
import socket

host = '127.0.0.1'
# port = 5000

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((host, port))

# def receive_message(display):
#     while True:
#         raw = client_socket.recv(1024)
#         if not raw:
#             print("")
#         data = raw.decode('utf-8')
#         print(data)
#         display.insert(END, data+"\n")

def submit(user_entry, entry, display):
    message = user_entry.get()
    entry.delete(0, END)
    message = message.lower().strip()
    display.insert(END, message+"\n")
    # client_socket.sendall(message.encode())

def client_program():
    root = Tk()
    root.geometry('500x350')
    user_entry = StringVar(value="")

    content = Frame(root, width=150)
    content.pack()
    name = Label(content, text="Chatroom")
    name.pack()
    info = Label(content, text=f"Connected to: {host}")
    info.pack()

    display = Text(content, height=15, width=50)
    display.pack()

    entry = Entry(content, textvariable=user_entry)
    entry.pack(side=LEFT, padx=50, pady=5)

    send_button = Button(content, command=lambda: submit(user_entry, entry, display), text="Send", width=10)
    send_button.pack(side=RIGHT, padx=50, pady=5)

    worker_thread = 
    root.mainloop()

if __name__ == '__main__':
    client_program()

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