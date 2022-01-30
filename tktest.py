from tkinter import *
from tkinter import ttk

def merge():
    print("success!")

height = 450
width = 600

root = Tk()
root.title("CremFuelled's PDF Merger")
root.geometry(f"{width}x{height}")

main_frame = ttk.Frame(root, padding="3 3 3 3")
main_frame.grid(row=0, column=0, sticky=(N, S, E, W))

label_1 = ttk.Label(main_frame, text="File:")
label_1.grid(row=1, column=1, sticky=(N, W))

#todo
text_field = ttk.Entry(main_frame, )

button = ttk.Button(main_frame, text="Merge!", command=merge)
button.grid(row=2, column=1, sticky=(W, E))

root.mainloop()