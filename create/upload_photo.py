from tkinter import filedialog
from PIL import Image as PilImage, ImageTk
import io

photo_data = None

def load_photo(photo_label):
    global photo_data
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filepath:
        with open(filepath, 'rb') as f:
            photo_data = f.read()
        img = PilImage.open(io.BytesIO(photo_data)).resize((100, 100))
        photo_label.img = ImageTk.PhotoImage(img)
        photo_label.configure(image=photo_label.img)
    return photo_data

