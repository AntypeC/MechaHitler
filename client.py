from tkinter import *
from tkinter import font, filedialog
import socket
from threading import Thread
from PIL import Image, ImageTk
# from tkinterdnd2 import DND_FILES, TkinterDnD
import imageio
import os, queue, time
import edge_tts
import pyaudio
from io import BytesIO
from pydub import AudioSegment
import ast
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, "./img/führer/grok-71d4db52-e556-4e72-8998-f1112a05fc40.jpg")
# server_path = os.path.join(script_dir, "./server.py")
video = imageio.get_reader("./img/führer/grok-video-bba23814-090d-4ad4-9309-b66c4da8f74a.mp4")

store_frame = queue.Queue(maxsize=10) # get 10 frames at most, pause update_frame() if full

host = '127.0.0.1'
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((host, port))
except ConnectionRefusedError:
    print("No server launched. Try again.")

# tts_engine = pyttsx3.init()
# voices = tts_engine.getProperty("voices")

# def speaking(string):
#     tts_engine.say(string)
#     tts_engine.runAndWait()

# def speaking(TEXT) -> None:
#     communicator = edge_tts.Communicate(TEXT, VOICE, boundary="WordBoundary")
#     audio_chunks = []

#     pyaudio_instance = pyaudio.PyAudio()
#     audio_stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

#     for chunk in communicator.stream_sync():
#         if chunk["type"] == "audio" and chunk["data"]:
#             audio_chunks.append(chunk["data"])
#             if len(audio_chunks) >= CHUNK_SIZE:
#                 play_audio_chunks(audio_chunks, audio_stream)
#                 audio_chunks.clear()

#     # Play the rest of the audio
#     play_audio_chunks(audio_chunks, audio_stream)

#     audio_stream.stop_stream()
#     audio_stream.close()
#     pyaudio_instance.terminate()

# def play_audio_chunks(chunks: list[bytes], stream: pyaudio.Stream) -> None:
#     stream.write(AudioSegment.from_mp3(BytesIO(b''.join(chunks))).raw_data) 

# image_generator = video.iter_data()
# count = 0
# speech_length_ticks = 0

# if you want to manually adjust the speed of the video playback
# def update_frame():
#     global image_generator, count
#     for i in range(round(speech_length_ticks)):
#         try:
#             image = next(image_generator)
#             store_frame.put(image)
#         except StopIteration:
#             print(f"finished iterating frames from video: {count+1} times")
#             image_generator = video.iter_data()
#             image = next(image_generator)
#             store_frame.put(image)
#             count+=1


VOICE="ja-JP-NanamiNeural"
CHUNK_SIZE = 20



def speaking(TEXT) -> None:
    global audio_chunks, audio_stream, pyaudio_instance, word_list
    communicator = edge_tts.Communicate(TEXT, VOICE, boundary="WordBoundary")
    audio_chunks = []
    word_boundary = []
    word_list = TEXT.split()
    offset_list = []
    duration_list = []

    pyaudio_instance = pyaudio.PyAudio()
    audio_stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    for chunk in communicator.stream_sync():
        # if chunk["type"] == "audio":
            # print("audio chunk")
            # print(chunk)
        if chunk["type"] == "WordBoundary":
            # word_list.append(chunk["text"])
            offset_list.append(chunk["offset"])
            duration_list.append(chunk["duration"])
            word_boundary.append(chunk)
        if chunk["type"] == "audio" and chunk["data"]:
            audio_chunks.append(chunk["data"])
            # if len(audio_chunks) >= CHUNK_SIZE:
                # play_audio_chunks(audio_chunks, audio_stream)
                # audio_chunks.clear()
    # Play the rest of the audio
    # print(word_boundary)
    # print(word_list)
    # print(offset_list)
    # print(duration_list)
    chat_container.configure(state="normal")
    chat_container.insert(END, "Führer: ", "name")
    chat_container.configure(state="disabled")
    # type_thread = Thread(target=responding, args=(chat_container, "end", word_list, offset_list, duration_list), daemon=False)
    # type_thread.start()
    anime(chat_container, "end", word_list, offset_list, duration_list)
    play_audio_chunks(audio_chunks, audio_stream)
    audio_chunks.clear()
    audio_stream.stop_stream()
    audio_stream.close()
    pyaudio_instance.terminate()

def play_audio_chunks(chunks: list[bytes], stream: pyaudio.Stream) -> None:
    stream.write(AudioSegment.from_mp3(BytesIO(b''.join(chunks))).raw_data) 


image_generator = video.iter_data()
count = 0

word_num = 0
start_time = 0
current_word = ""
checked_time = False
is_fuhrer_typing = False

def anime(widget, index, word_list, offset_list, duration_list):
    global image_generator, count, word_num, start_time, current_word, checked_time, is_fuhrer_typing
    is_fuhrer_typing = True
    if checked_time == False:
            start_time = time.perf_counter_ns()
            checked_time = True
    TEXT = word_list[word_num]
    current_offset = offset_list[word_num]/10_000_000 # edge tts uses 100 nanoseconds
    time_diff = (time.perf_counter_ns() - start_time)/1_000_000_000 # time.perf_counter_ns() uses nanoseconds
    if time_diff < current_offset:
            widget.after(int((current_offset-time_diff)*1000), anime, widget, index, word_list, offset_list, duration_list)
    else:
        widget.configure(state="normal")
        if len(TEXT) > 0:
            widget.insert(index, TEXT[0])
            current_word += TEXT[0]
            delay = (duration_list[word_num]/len(TEXT))/10_000_000
            try:
                image = next(image_generator)
                store_frame.put(image)
            except StopIteration:
                print(f"finished iterating frames from video: {count+1} times")
                image_generator = video.iter_data()
                image = next(image_generator)
                store_frame.put(image)
                count+=1
            # if len(" ".join(word_list))-(len(word_list)-1) > 1:
            index = widget.index(f"{index} + 1 char")
            word_list[word_num] = TEXT[1:]
            widget.after(int(delay*1000), anime, widget, index, word_list, offset_list, duration_list)
        else:
            if word_num != len(word_list)-1:
                widget.insert(index, " ")
                word_num +=1
                current_word = ""
                widget.after(0, anime, widget, index, word_list, offset_list, duration_list)
            else:
                chat_container.insert(END, "\n")
                word_num = 0
                start_time = 0
                current_word = ""
                checked_time = False
                is_fuhrer_typing = False
                entry.configure(state="normal")
                entry.delete(0, END)
                chat_container.configure(state="disabled")
                chat_container.see("end")

def receive_message():
    while True:
        raw = client_socket.recv(1024)
        if not raw:
            print("")
        else:
            data = raw.decode('utf-8')
            print(data)
            # speech_length_ticks = len(data)*1.1
            # sub_thread = Thread(target=update_frame, daemon=True)
            # sub_thread.start()

            # responding(chat_container, "end", data+"\n")
            speaking(data)

def submit(user_entry):
    message = user_entry.get()
    message = message.lower().strip()
    entry.delete(0, END)
    client_socket.sendall(message.encode())
    chat_container.configure(state="normal")
    chat_container.insert(END, "Goy: ", "name")
    chat_container.insert(END, message+"\n")
    chat_container.configure(state="disabled")
    chat_container.see("end")

dot_counter = 0
def update_gui():
    global dot_counter
    if is_fuhrer_typing==True:
        dot_counter+=1
        entry.delete(0, END)
        entry.insert(0, "Führer is responding...")
        entry.configure(state="disabled")
    if store_frame.empty():
        dot_counter=0
        insert_image.after(33, update_gui)
    else:
        current_frame = store_frame.get_nowait()
        tk_image = ImageTk.PhotoImage(Image.fromarray(current_frame))
        insert_image.config(image=tk_image)
        insert_image.image = tk_image
        insert_image.after(33, update_gui)

root = Tk()
root.geometry('2000x1200')
root.title("MechaHitler")
user_entry = StringVar(value="")

if "Blankenburg_UNZ1A" in font.families():
    fraktur_font = font.Font(family="Blankenburg_UNZ1A", size=20, slant="italic")
else:
    fraktur_font = font.Font(family="Arial", size=16, slant="italic")

def clear_history():
    chat_container.configure(state="normal")
    chat_container.delete("1.0", END)
    chat_container.configure(state="disabled")

def load_history():
    chat_history = filedialog.askopenfile()
    if chat_history != None:
        clear_history()
        read_file = chat_history.read() # reads data and turns into string
        chatlog_json = ast.literal_eval(read_file) # detects patterns in string and turn it into list
        converted_to_string = json.dumps(chatlog_json) # runs list into string with correct formatting
        client_socket.sendall(converted_to_string.encode())

        print(chatlog_json)
        print(type(chatlog_json))
        chat_container.configure(state="normal")
        for i in chatlog_json:
            print(i)
            if i["role"] == "system":
                continue
            elif i["role"] == "user":
                chat_container.insert(END, "Goy: ", "name")
            elif i["role"] == "assistant":
                chat_container.insert(END, "Führer: ", "name")
            chat_container.insert(END, i["content"].strip()+"\n")
        chat_container.configure(state="disabled")
        chat_history.close()

BRIGHT = {
    "root":            "#E8E8E8",
    "top_frame":       "#E8E8E8",
    "bottom_frame":    "#DCDCDC",
    "menubar":         "#E8E8E8",
    "settings":        "#F4F4F4",
    "roles":           "#F4F4F4",
    "name_bg":         "#E8E8E8",
    "name_fg":         "#1A1A1A",
    "chat_bg":         "#FFFFFF",
    "chat_fg":         "#111111",
    "chat_insert":     "#111111",
    "entry_bg":        "#FFFFFF",
    "entry_fg":        "#111111",
    "entry_insert":    "#8B1A1A",
    "button_bg":       "#E0E0E0",
    "button_fg":       "#111111",
    "button_active":   "#C9C9C9",
    "accent":          "#7A1515",
    "select_bg":       "#C9B896",
    "select_fg":       "#111111",
}

DARK = {
    "root":            "#16191F",
    "top_frame":       "#16191F",
    "bottom_frame":    "#1F232B",
    "menubar":         "#1F232B",
    "settings":        "#272C36",
    "roles":           "#272C36",
    "name_bg":         "#16191F",
    "name_fg":         "#D4C4A0",
    "chat_bg":         "#22272F",
    "chat_fg":         "#EDE4D4",
    "chat_insert":     "#EDE4D4",
    "entry_bg":        "#2C323C",
    "entry_fg":        "#F3EADF",
    "entry_insert":    "#C94A3A",
    "button_bg":       "#3A414C",
    "button_fg":       "#EDE4D4",
    "button_active":   "#B33A2C",
    "accent":          "#B33A2C",
    "select_bg":       "#6E3A2A",
    "select_fg":       "#F7EFE0",
}

dark_mode=False

def apply_theme():
    global dark_mode
    if dark_mode==False:
        print("hello??")
        dark_mode=True
        c=DARK
    else:
        dark_mode=False
        c=BRIGHT
    root.configure(bg=c["root"])
    top_frame.configure(bg=c["top_frame"])
    bottom_frame.configure(bg=c["bottom_frame"])

    menubar.configure(bg=c["menubar"], fg=c["chat_fg"],
                      activebackground=c["accent"], activeforeground=c["select_fg"])
    settings.configure(bg=c["settings"], fg=c["chat_fg"],
                       activebackground=c["accent"], activeforeground=c["select_fg"])
    roles.configure(bg=c["roles"], fg=c["chat_fg"],
                    activebackground=c["accent"], activeforeground=c["select_fg"])

    name.configure(bg=c["name_bg"], fg=c["name_fg"])
    insert_image.configure(bg=c["top_frame"])

    chat_container.configure(
        bg=c["chat_bg"],
        fg=c["chat_fg"],
        insertbackground=c["chat_insert"],
        selectbackground=c["select_bg"],
        selectforeground=c["select_fg"],
        highlightbackground=c["top_frame"],
        highlightcolor=c["accent"],
    )
    chat_container.tag_configure("name", foreground=c["accent"])

    entry.configure(
        bg=c["entry_bg"],
        fg=c["entry_fg"],
        insertbackground=c["entry_insert"],
        highlightbackground=c["accent"],
        highlightcolor=c["accent"],
    )

    send_button.configure(
        bg=c["button_bg"],
        fg=c["button_fg"],
        activebackground=c["button_active"],
        activeforeground=c["select_fg"],
        highlightbackground=c["accent"],
    )

def build_gui():
    global top_frame, bottom_frame, menubar, root, settings, roles, name, insert_image, chat_container, entry, send_button

    top_frame = Frame(root)
    top_frame.pack(fill="both", expand=True)

    bottom_frame = Frame(top_frame)
    bottom_frame.pack(side="bottom", fill="x")

    menubar = Menu(root)
    root.config(menu=menubar)
    settings = Menu(menubar, tearoff=0)
    roles = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="⚙️ Preferences", menu=settings)
    menubar.add_cascade(label="🎭 Roles", menu=roles)
    settings.add_command(label="Load History", command=load_history)
    settings.add_command(label="Reset Session", command=clear_history)
    settings.add_command(label="Dark Mode", command=apply_theme)
    settings.add_separator()
    settings.add_command(label="Exit", command=root.destroy)

    name = Label(top_frame, text='"Ein Volk, ein Reich, ein Führer"', font=fraktur_font)
    name.pack(side="top")

    img = Image.open(img_path)
    img.thumbnail((768, 1168))
    tk_image = ImageTk.PhotoImage(img)
    insert_image = Label(top_frame, image=tk_image)
    insert_image.image = tk_image
    insert_image.pack(side="right")

    chat_container = Text(top_frame, font=("serif", 15), height=25, width=120)
    chat_container.tag_configure("name", font=fraktur_font)
    chat_container.configure(state="disabled")
    chat_container.pack(side="left", fill="both", expand=True, padx=10, pady=(5, 5))

    entry = Entry(bottom_frame, font=("serif", 16), textvariable=user_entry)
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