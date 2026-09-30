import customtkinter as ctk
from PIL import Image
import subprocess
import sys
import os


# =========================================================
# CUSTOMTKINTER SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# PATHS
# =========================================================

# Folder where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Important project paths
BACKGROUND_FILE = os.path.join(
    BASE_DIR,
    "imgs",
    "background.png"
)

PROFILE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "profile.json"
)

TODO_FILE = os.path.join(
    BASE_DIR,
    "todo.py"
)

ACC_FILE = os.path.join(
    BASE_DIR,
    "acc.py"
)


# =========================================================
# APP
# =========================================================

app = ctk.CTk()

app.title("Orbit")

app.attributes("-fullscreen", True)

app.minsize(
    800,
    600
)

# ESC = close
app.bind(
    "<Escape>",
    lambda event: app.destroy()
)


# =========================================================
# BACKGROUND
# =========================================================

try:

    original_image = Image.open(
        BACKGROUND_FILE
    )

except FileNotFoundError:

    print(
        f"Background image not found:\n{BACKGROUND_FILE}"
    )

    app.destroy()
    sys.exit()


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


# =========================================================
# BACKGROUND RESIZE
# =========================================================

last_width = 0
last_height = 0


def resize_background(event):

    global last_width
    global last_height

    # Only react to the main window
    if event.widget != app:
        return

    window_width = event.width
    window_height = event.height

    if window_width <= 0 or window_height <= 0:
        return

    # Prevent unnecessary resizing
    if (
        window_width == last_width
        and
        window_height == last_height
    ):
        return

    last_width = window_width
    last_height = window_height

    # Original image size
    image_width, image_height = original_image.size

    # Calculate scale
    scale = max(
        window_width / image_width,
        window_height / image_height
    )

    new_width = int(
        image_width * scale
    )

    new_height = int(
        image_height * scale
    )

    # Resize image
    resized_image = original_image.resize(
        (
            new_width,
            new_height
        ),
        Image.Resampling.LANCZOS
    )

    # Center crop
    left = (
        new_width - window_width
    ) // 2

    top = (
        new_height - window_height
    ) // 2

    right = (
        left + window_width
    )

    bottom = (
        top + window_height
    )

    cropped_image = resized_image.crop(
        (
            left,
            top,
            right,
            bottom
        )
    )

    # Convert image for CustomTkinter
    bg_image = ctk.CTkImage(
        light_image=cropped_image,
        dark_image=cropped_image,
        size=(
            window_width,
            window_height
        )
    )

    background_label.configure(
        image=bg_image
    )

    # Keep reference so image doesn't disappear
    background_label.bg_image = bg_image


# Listen for window resizing
app.bind(
    "<Configure>",
    resize_background
)


# =========================================================
# OPEN NEXT PAGE
# =========================================================

def open_page(file_path):

    # Check if the Python file exists
    if not os.path.exists(file_path):

        print(
            f"File not found:\n{file_path}"
        )

        return

    try:

        subprocess.Popen(
            [
                sys.executable,
                file_path
            ],
            cwd=BASE_DIR
        )

        # Close current window
        app.destroy()

    except OSError as error:

        print(
            f"Could not open {file_path}"
        )

        print(error)


# =========================================================
# GET STARTED
# =========================================================

def on_button_click():

    # If profile already exists
    if os.path.exists(PROFILE_FILE):

        open_page(
            TODO_FILE
        )

    # If profile does not exist
    else:

        open_page(
            ACC_FILE
        )


# =========================================================
# GET STARTED BUTTON
# =========================================================

button = ctk.CTkButton(
    app,

    text="GET STARTED",

    fg_color="#0B3D91",

    hover_color="#1261D6",

    text_color="#FFFFFF",

    border_color="#35C2FF",

    border_width=1,

    corner_radius=12,

    font=(
        "Segoe UI",
        16,
        "bold"
    ),

    width=400,

    height=60,

    command=on_button_click
)

button.place(
    relx=0.5,
    rely=0.4,
    anchor="center",

    relwidth=0.3,

    relheight=0.075
)


# =========================================================
# START APP
# =========================================================

app.mainloop()