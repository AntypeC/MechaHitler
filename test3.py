import tkinter as tk
from PIL import Image, ImageTk  # Requires 'pip install pillow'

root = tk.Tk()
root.title("Text Box with Image Background")
root.geometry("400x200")

# 1. Load your background image using Pillow
bg_image = Image.open("./img/jesus_the_warrior.png")  # Replace with your image file
bg_photo = ImageTk.PhotoImage(bg_image)

# 2. Create a Canvas to hold the background image
canvas = tk.Canvas(root, width=300, height=40, bd=0, highlightthickness=0)
canvas.pack(pady=50)

# 3. Add the image to the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# 4. Create a borderless Entry widget with a flat background
# Note: Changing 'bg' to match your image's dominant color prevents clipping artifacts
entry = tk.Entry(root, font=("Helvetica", 14), bd=0, bg="white", highlightthickness=0)

# 5. Embed the entry widget directly inside the canvas item space
canvas.create_window(10, 8, window=entry, anchor="nw", width=280, height=24)

root.mainloop()