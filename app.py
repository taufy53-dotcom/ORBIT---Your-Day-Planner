import customtkinter as ctk
from PIL import Image
import subprocess
import sys
import os


# -----------------------------
# CustomTkinter settings
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -----------------------------
# App
# -----------------------------
app = ctk.CTk()
app.title("Orbit")
app.attributes("-fullscreen", True)
app.minsize(800, 600)
app.bind("<Escape>", lambda e: app.destroy())

# -----------------------------
# Load original background
# -----------------------------
original_image = Image.open("imgs/background.png")

# Background label
background_label = ctk.CTkLabel(
    app,
    text=""
)

background_label.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)


# -----------------------------
# Resize + crop background
# -----------------------------
def resize_background(event):

    window_width = event.width
    window_height = event.height

    # Original image dimensions
    image_width, image_height = original_image.size

    # Calculate scale needed to completely cover window
    scale = max(
        window_width / image_width,
        window_height / image_height
    )

    new_width = int(image_width * scale)
    new_height = int(image_height * scale)

    # Resize while keeping aspect ratio
    resized_image = original_image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    # Center crop
    left = (new_width - window_width) // 2
    top = (new_height - window_height) // 2

    right = left + window_width
    bottom = top + window_height

    cropped_image = resized_image.crop(
        (left, top, right, bottom)
    )

    # Convert for CustomTkinter
    bg_image = ctk.CTkImage(
        light_image=cropped_image,
        dark_image=cropped_image,
        size=(window_width, window_height)
    )

    background_label.configure(
        image=bg_image
    )

    # Keep reference
    background_label.bg_image = bg_image


# Detect window resizing
app.bind("<Configure>", resize_background)


def on_button_click():

    if(os.path.exists("data/profile.json")):
        subprocess.Popen([sys.executable, "todo.py"])
    else:
        subprocess.Popen([sys.executable, "acc.py"])

    # Close the current window
    app.destroy()
    

button = ctk.CTkButton(
    app,
    text="GET STARTED",
    fg_color="#0B3D91",
    hover_color="#1261D6",
    text_color="#FFFFFF",
    border_color="#35C2FF",
    border_width=1,
    corner_radius=12,
    font=("Segoe UI", 16, "bold"),
    width = 400,
    height = 60,
    command = on_button_click
)

button.place(relx = 0.5, rely = 0.4, anchor = "center", relwidth = 0.3, relheight = 0.075)

# -----------------------------
# Run
# -----------------------------
app.mainloop()