import tkinter as tk
from tkinter import filedialog

def open_file():
    filepath = filedialog.askopenfilename(
        initialdir="/", 
        title="Select file",
        filetypes=(("Text files", "*.txt"), ("all files", "*.*"))
    )
    if filepath:
        with open(filepath, 'r') as f:
            content = f.read()
            text_area.delete("1.0", tk.END) # Clear previous text
            text_area.insert(tk.END, content) # Insert new content
            
root = tk.Tk()
root.title("File Input Example")

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack()

text_area = tk.Text(root)
text_area.pack()

root.mainloop()