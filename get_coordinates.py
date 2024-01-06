import tkinter as tk
from PIL import Image, ImageTk

def on_drag(event):
    global rect, start_x, start_y, curX, curY
    curX, curY = event.x, event.y
    canvas.coords(rect, start_x, start_y, curX, curY)

def on_press(event):
    global start_x, start_y, rect
    start_x = event.x
    start_y = event.y
    rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')

def on_release(event):
    global rect, start_x, start_y, curX, curY
    # Final rectangle coordinates
    print(f"Rectangle coordinates: (top-left) {start_x}, {start_y} (bottom-right) {curX}, {curY}")
    # Additional functionality can be added here

def main():
    global canvas
    root = tk.Tk()

    # Load the image
    image_path = 'images/page_2.png'  # Replace with the path to your image
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Create a canvas to display the image and capture mouse events
    canvas = tk.Canvas(root, width=photo.width(), height=photo.height())
    canvas.pack()

    # Display the image
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Bind mouse events to functions
    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()

if __name__ == "__main__":
    main()