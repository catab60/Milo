import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, radius=20, bg="#007acc", width=200, height=150, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0, **kwargs)

        self.radius = radius
        self.width = width
        self.height = height
        self.bg = bg

        # Create the rounded frame with rounded corners
        self._create_rounded_frame()

    def _create_rounded_frame(self):
        """Create a rounded frame background."""
        # Create an image for the rounded frame
        frame_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_image)

        # Draw the rounded corners manually
        draw.rectangle([self.radius, 0, self.width - self.radius, self.height], fill=self.bg)  # top bar
        draw.rectangle([0, self.radius, self.width, self.height - self.radius], fill=self.bg)  # left & right bars
        draw.pieslice([0, 0, self.radius * 2, self.radius * 2], 180, 270, fill=self.bg)  # top-left corner
        draw.pieslice([self.width - self.radius * 2, 0, self.width, self.radius * 2], 270, 360, fill=self.bg)  # top-right corner
        draw.pieslice([0, self.height - self.radius * 2, self.radius * 2, self.height], 90, 180, fill=self.bg)  # bottom-left corner
        draw.pieslice([self.width - self.radius * 2, self.height - self.radius * 2, self.width, self.height], 0, 90, fill=self.bg)  # bottom-right corner

        # Convert the image to a format Tkinter can use
        self.frame_image = ImageTk.PhotoImage(frame_image)

        # Place the image on the canvas as the background
        self.create_image(0, 0, anchor="nw", image=self.frame_image)

    def add_widget(self, widget, **kwargs):
        """Add a widget to the frame (using place)."""
        widget.place(in_=self, **kwargs)


# Example usage of the RoundedFrame
root = tk.Tk()
root.title("Nested Rounded Frame Example")
root.geometry("600x400")

# Create a RoundedFrame (outer)
outer_frame = RoundedFrame(
    root,
    radius=30,
    bg="#28a745",
    width=500,
    height=300
)
outer_frame.pack(pady=20)

# Create a RoundedFrame (inner)
inner_frame = RoundedFrame(
    outer_frame,  # Parent is the outer_frame
    radius=30,
    bg="#007acc",
    width=400,
    height=200
)
inner_frame.place(x=50, y=50)

# Add some widgets to the inner frame
label = tk.Label(inner_frame, text="This is inside the inner rounded frame", font=("Arial", 14), fg="white", bg="#007acc")
label.place(x=50, y=50)

button = tk.Button(inner_frame, text="Click Me", command=lambda: print("Button clicked"))
button.place(x=100, y=120)

root.mainloop()
