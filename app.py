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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------
# DEVELOPMENT PATHS
# ---------------------------------------------------------

BACKGROUND_FILE = os.path.join(
    BASE_DIR,
    "imgs",
    "background.png"
)

PROFILE_FILE = os.path.join(
    os.environ.get(
        "APPDATA",
        os.path.expanduser("~")
    ),
    "Orbit",
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


# ---------------------------------------------------------
# INSTALLED APPLICATION PATHS
# ---------------------------------------------------------

INSTALL_DIR = os.path.dirname(
    sys.executable
)

TODO_EXE = os.path.join(
    INSTALL_DIR,
    "OrbitTodo.exe"
)

ACC_EXE = os.path.join(
    INSTALL_DIR,
    "OrbitAccount.exe"
)


# Create user data directory
os.makedirs(
    os.path.dirname(PROFILE_FILE),
    exist_ok=True
)


# =========================================================
# APP
# =========================================================

app = ctk.CTk()

app.title("Orbit")

app.attributes(
    "-fullscreen",
    True
)

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

except Exception as error:

    print(
        f"Could not load background:\n{error}"
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

    if event.widget != app:
        return

    window_width = event.width
    window_height = event.height

    if window_width <= 0 or window_height <= 0:
        return

    if (
        window_width == last_width
        and
        window_height == last_height
    ):
        return

    last_width = window_width
    last_height = window_height

    image_width, image_height = original_image.size

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

    resized_image = original_image.resize(
        (
            new_width,
            new_height
        ),
        Image.Resampling.LANCZOS
    )

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

    background_label.bg_image = bg_image


app.bind(
    "<Configure>",
    resize_background
)


# =========================================================
# OPEN NEXT PAGE
# =========================================================

def open_page(
    python_file,
    executable_file
):

    try:

        # -------------------------------------------------
        # INSTALLED VERSION
        # -------------------------------------------------

        if getattr(
            sys,
            "frozen",
            False
        ):

            if not os.path.exists(
                executable_file
            ):

                print(
                    "Application not found:"
                )

                print(
                    executable_file
                )

                return

            print(
                f"Launching:\n{executable_file}"
            )

            subprocess.Popen(
                [executable_file],
                cwd=os.path.dirname(
                    executable_file
                )
            )


        # -------------------------------------------------
        # DEVELOPMENT VERSION
        # -------------------------------------------------

        else:

            if not os.path.exists(
                python_file
            ):

                print(
                    "Python file not found:"
                )

                print(
                    python_file
                )

                return

            print(
                f"Launching:\n{python_file}"
            )

            subprocess.Popen(
                [
                    sys.executable,
                    python_file
                ],
                cwd=BASE_DIR
            )


        # Close current application
        app.destroy()


    except Exception as error:

        print(
            "Could not launch application:"
        )

        print(error)


# =========================================================
# GET STARTED
# =========================================================

def on_button_click():

    print(
        "GET STARTED clicked"
    )

    print(
        f"Profile file:\n{PROFILE_FILE}"
    )


    # -----------------------------------------------------
    # PROFILE EXISTS
    # -----------------------------------------------------

    if os.path.exists(
        PROFILE_FILE
    ):

        print(
            "Profile found."
        )

        # Open Todo
        open_page(
            TODO_FILE,
            TODO_EXE
        )


    # -----------------------------------------------------
    # PROFILE DOES NOT EXIST
    # -----------------------------------------------------

    else:

        print(
            "Profile not found."
        )

        # Open Account
        open_page(
            ACC_FILE,
            ACC_EXE
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
