import tkinter as tk

root = tk.Tk()
root.title("Layout Example")
root.geometry("500x300")

# 1. Main Textbox at the top
textbox = tk.Text(root, height=10)
# fill="both" and expand=True allows it to take up all remaining top space
textbox.pack(fill="both", expand=True, padx=10, pady=(10, 5))

# 2. Bottom Container Frame (this spans the full width)
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="x", padx=10, pady=(5, 10))

# 3. Entry widget inside the bottom frame (aligned left)
# expand=True allows the entry box to stretch and fill the extra space
entry = tk.Entry(bottom_frame)
entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

# 4. Button widget inside the bottom frame (aligned right)
button = tk.Button(bottom_frame, text="Submit")
button.pack(side="right", padx=(5, 0))

root.mainloop()
