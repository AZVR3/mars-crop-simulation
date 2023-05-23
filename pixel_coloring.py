# Importing the modules
import random
import tkinter as tk

# Creating the canvas
canvas = tk.Canvas(width=500, height=500)
canvas.pack()

# Initializing the colors and the pixels
colors = ["green"]
pixels = set()

# Defining the function to color a random pixel
def color_pixel():
    # Generating a random coordinate and color
    x = random.randint(0, 31)
    y = random.randint(0, 31)
    color = random.choice(colors)

    # Checking if the pixel is already colored
    if (x, y) not in pixels:
        # Coloring the pixel and adding it to the set
        canvas.create_rectangle(x * 16, y * 16, x * 16 + 16, y * 16 + 16, fill=color)
        pixels.add((x, y))

    # Checking if the canvas is filled up
    if len(pixels) == 1024:
        # Stopping the loop
        return
    else:
        # Repeating the function after 1 millisecond
        canvas.after(1, color_pixel)

# Calling the function
color_pixel()

# Running the main loop
tk.mainloop()
