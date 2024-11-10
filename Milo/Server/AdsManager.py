import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image

class AdsManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Ads Manager")
        self.root.geometry("400x350")
        
        self.image_path = None

        tk.Label(root, text="Views:").pack(pady=5)
        self.views_entry = tk.Entry(root, width=40)
        self.views_entry.pack(pady=5)

        tk.Button(root, text="Select Ad Banner", command=self.select_image).pack(pady=10)

        self.image_label = tk.Label(root, text="Must be ")
        self.image_label.pack(pady=5)

        tk.Button(root, text="Calculate Cost", command=self.calculate_cost).pack(pady=10)
        self.cost_label = tk.Label(root, text="Cost: $0.00")
        self.cost_label.pack(pady=5)

        tk.Button(root, text="Save Ad", command=self.save_ad).pack(pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.image_label.config(text=f"Selected: {self.image_path.split('/')[-1]}")
        else:
            self.image_label.config(text="No Image Selected")

    def calculate_cost(self):
        try:
            views = int(self.views_entry.get())
            cost = views * 0.25
            self.cost_label.config(text=f"Cost: ${cost:.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of views.")

    def save_ad(self):
        if not self.image_path:
            messagebox.showerror("No Image Selected", "Please select an image before saving.")
            return
        
        try:
            views = int(self.views_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of views.")
            return

        # Create the "ads" directory if it doesn't exist
        if not os.path.exists("ads"):
            os.makedirs("ads")

        # Determine the next available ID
        existing_files = os.listdir("ads")
        available_id = 1
        for file in existing_files:
            try:
                file_id = int(file.split("_")[0])
                available_id = max(available_id, file_id + 1)
            except (IndexError, ValueError):
                continue

        # Construct the filename
        filename = f"{available_id}_0_{views}.png"
        save_path = os.path.join("ads", filename)

        # Save the image
        try:
            image = Image.open(self.image_path)
            image.save(save_path)
            messagebox.showinfo("Ad Saved", f"Ad saved successfully as {filename} in the 'ads' folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdsManager(root)
    root.mainloop()
