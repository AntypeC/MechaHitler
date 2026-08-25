from tkinter import *
from tkinter import font
import socket
from threading import Thread
from PIL import Image, ImageTk
# from tkinterdnd2 import DND_FILES, TkinterDnD
import imageio
import os, queue, time
import pyttsx3

script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, "./img/führer/default.jpg")
# server_path = os.path.join(script_dir, "./server.py")
video = imageio.get_reader("./img/führer/speech.mp4")

store_frame = queue.Queue(maxsize=10) # get 10 frames at most, pause update_frame() if full

host = '127.0.0.1'
port = 5000

tts_engine = pyttsx3.init()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((host, port))
except ConnectionRefusedError:
    print("No server launched. Try again.")


image_generator = video.iter_data()
count = 0
speech_length_ticks = 0

def update_frame():
    global image_generator, count
    for i in range(round(speech_length_ticks)):
        try:
            image = next(image_generator)
            store_frame.put(image)
        except StopIteration:
            print(f"finished iterating frames from video: {count+1} times")
            image_generator = video.iter_data()
            image = next(image_generator)
            store_frame.put(image)
            count+=1
    # try:
    #     for image in video.iter_data():
    #         store_frame.put(image) # put image inside Queue inside update_frame function ran inside a subthread
    # except StopIteration:
    #     print("finished iterating video frames")

def speaking(string):
    tts_engine.say(string)
    tts_engine.runAndWait()

def messaging(widget, index, string):
    widget.configure(state="normal")
    if len(string) > 0:
        widget.insert(index, string[0])
        if len(string) > 1:
            index = widget.index("%s + 1 char" % index)
            widget.after(50, messaging, widget, index, string[1:])
    widget.configure(state="disabled")

def receive_message():
    global speech_length_ticks
    while True:
        raw = client_socket.recv(1024)
        if not raw:
            print("")
        data = raw.decode('utf-8').lower()
        print(data)
        speech_length_ticks = len(data)*1.1
        sub_thread = Thread(target=update_frame, daemon=True)
        sub_thread.start()

        chat_container.configure(state="normal")
        chat_container.insert(END, "Führer: ")
        chat_container.configure(state="disabled")

        messaging(chat_container, "end", data+"\n")
        speaking(data)

def submit(user_entry):
    message = user_entry.get()
    message = message.lower().strip()
    entry.delete(0, END)
    client_socket.sendall(message.encode())
    chat_container.configure(state="normal")
    chat_container.insert(END, "You: "+message+"\n")
    chat_container.configure(state="disabled")

def update_gui():
    chat_container.see("end")
    if store_frame.empty():
        insert_image.after(32, update_gui)
    else:
        current_frame = store_frame.get_nowait()
        tk_image = ImageTk.PhotoImage(Image.fromarray(current_frame))
        insert_image.config(image=tk_image)
        insert_image.image = tk_image
        insert_image.after(32, update_gui)

root = Tk()
root.geometry('2000x1200')
root.title("MechaHitler")
user_entry = StringVar(value="")

def build_gui():
    global chat_container, entry, insert_image

    top_frame = Frame(root)
    top_frame.pack(fill="both", expand=True)

    name = Label(top_frame, text="'Ein Volk, ein Reich, ein Führer'", font=("Helvetica", 14, "italic"))
    name.pack(side="top")

    bottom_frame = Frame(top_frame)
    bottom_frame.pack(side="bottom", fill="x")

    img = Image.open(img_path)
    # img.thumbnail((768, 1168))
    tk_image = ImageTk.PhotoImage(img)
    insert_image = Label(top_frame, image=tk_image)
    insert_image.image = tk_image
    insert_image.pack(side="right")

    faktur_font = font.Font(family="UnifrakturMaguntia", size=18)

    chat_container = Text(top_frame, font=faktur_font, height=25, width=120)
    chat_container.configure(state="disabled")
    chat_container.pack(side="left", fill="both", expand=True, padx=10, pady=(5, 5))

    entry = Entry(bottom_frame, font=("Arial", 18), textvariable=user_entry)
    entry.pack(side=LEFT, fill="x", expand=True, padx=10, pady=(10, 5))

    send_button = Button(bottom_frame, command=lambda: submit(user_entry), text="Send", width=10)
    send_button.pack(side=RIGHT, padx=10, pady=(10, 5))

    recv_thread = Thread(target=receive_message, daemon=True)
    recv_thread.start()

    root.bind("<Return>", lambda event: submit(user_entry))

    update_gui()


if __name__ == "__main__":
    build_gui()
    root.mainloop()