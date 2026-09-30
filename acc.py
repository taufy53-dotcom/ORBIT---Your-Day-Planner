import customtkinter as ctk
from PIL import Image
import json
import subprocess
import sys
import os


# =========================================================
# APP
# =========================================================

app = ctk.CTk()
app.title("Orbit - Account Details")
app.geometry("1000x700")

app.bind("<Escape>", lambda e: app.destroy())


# =========================================================
# COLORS
# =========================================================

BACKGROUND = "#071426"
CARD = "#0D2038"
BLUE = "#0B3D91"
BLUE_HOVER = "#1261D6"
CYAN = "#35C2FF"
TEXT = "#FFFFFF"
SECONDARY = "#7D91A8"
BORDER = "#1B4F7A"


# =========================================================
# JSON FILE
# =========================================================

# =========================================================
# JSON FILE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

# Create data folder if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

TODO_FILE = os.path.join(BASE_DIR, "todo.py")

PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")


# =========================================================
# BACKGROUND
# =========================================================

bg_image = ctk.CTkImage(
    light_image=Image.open("imgs/acc.png"),
    dark_image=Image.open("imgs/acc.png"),
    size=(1000, 800)
)

bg_label = ctk.CTkLabel(
    app,
    text="",
    image=bg_image
)

bg_label.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

bg_label.bg_image = bg_image


# =========================================================
# REGISTRATION CARD
# =========================================================

card = ctk.CTkFrame(
    app,
    width=500,
    height=650,                
    fg_color=CARD,
    corner_radius=1,
    border_width=1,
    border_color=BORDER
)

card.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

card.pack_propagate(False)


# =========================================================
# TITLE
# =========================================================

title = ctk.CTkLabel(
    card,
    text="CREATE YOUR ORBIT PROFILE",
    font=("Segoe UI", 25, "bold"),
    text_color=TEXT
)

title.pack(
    pady=(30, 5)
)


# =========================================================
# SUBTITLE
# =========================================================

subtitle = ctk.CTkLabel(
    card,
    text="Enter your details to get started",
    font=("Segoe UI", 13),
    text_color=SECONDARY
)

subtitle.pack(
    pady=(0, 18)
)


# =========================================================
# NAME
# =========================================================

name_entry = ctk.CTkEntry(
    card,
    placeholder_text="Full Name",
    width=400,
    height=45,
    font=("Segoe UI", 15),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

name_entry.pack(pady=6)


# =========================================================
# DATE OF BIRTH
# =========================================================

dob_entry = ctk.CTkEntry(
    card,
    placeholder_text="Date of Birth (DD-MM-YYYY)",
    width=400,
    height=45,
    font=("Segoe UI", 15),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

dob_entry.pack(pady=6)


# =========================================================
# EMAIL
# =========================================================

email_entry = ctk.CTkEntry(
    card,
    placeholder_text="Email Address",
    width=400,
    height=45,
    font=("Segoe UI", 15),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

email_entry.pack(pady=6)


# =========================================================
# USERNAME
# =========================================================

username_entry = ctk.CTkEntry(
    card,
    placeholder_text="Username",
    width=400,
    height=45,
    font=("Segoe UI", 15),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

username_entry.pack(pady=6)


# =========================================================
# PHONE
# =========================================================

phone_entry = ctk.CTkEntry(
    card,
    placeholder_text="Phone Number (Optional)",
    width=400,
    height=45,
    font=("Segoe UI", 15),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

phone_entry.pack(pady=6)


# =========================================================
# STATUS MESSAGE
# =========================================================

status_label = ctk.CTkLabel(
    card,
    text="",
    font=("Segoe UI", 12),
    text_color=CYAN
)

status_label.pack(
    pady=(5, 5)
)


# =========================================================
# SAVE PROFILE
# =========================================================

def save_profile():

    name = name_entry.get().strip()
    dob = dob_entry.get().strip()
    email = email_entry.get().strip()
    username = username_entry.get().strip()
    phone = phone_entry.get().strip()

    # -----------------------------------------
    # CHECK REQUIRED FIELDS
    # -----------------------------------------

    if not name:
        status_label.configure(
            text="Please enter your name.",
            text_color="#FF6B6B"
        )
        name_entry.focus()
        return

    if not dob:
        status_label.configure(
            text="Please enter your date of birth.",
            text_color="#FF6B6B"
        )
        dob_entry.focus()
        return

    if not email:
        status_label.configure(
            text="Please enter your email.",
            text_color="#FF6B6B"
        )
        email_entry.focus()
        return

    if not username:
        status_label.configure(
            text="Please enter a username.",
            text_color="#FF6B6B"
        )
        username_entry.focus()
        return

    # -----------------------------------------
    # CREATE PROFILE DATA
    # -----------------------------------------

    profile = {
        "name": name,
        "dob": dob,
        "email": email,
        "username": username,
        "phone": phone
    }

    # -----------------------------------------
    # SAVE TO JSON
    # -----------------------------------------

    try:

        with open(
            PROFILE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                indent=4,
                ensure_ascii=False
            )

        status_label.configure(
            text="✓ Profile saved successfully!",
            text_color=CYAN
        )

        subprocess.Popen([sys.executable, TODO_FILE])

    except OSError as error:

        status_label.configure(
            text="Could not save profile.",
            text_color="#FF6B6B"
        )

        print(error)


# =========================================================
# CREATE PROFILE BUTTON
# =========================================================

save_button = ctk.CTkButton(
    card,
    text="CREATE PROFILE",
    width=400,
    height=45,                  # FIXED: proper button height
    font=("Segoe UI", 15, "bold"),
    fg_color=BLUE,
    hover_color=BLUE_HOVER,
    text_color=TEXT,
    corner_radius=8,
    command=save_profile
)

save_button.pack(
    pady=(10, 25)
)


# =========================================================
# ENTER KEY
# =========================================================

app.bind(
    "<Return>",
    lambda event: save_profile()
)


# =========================================================
# START
# =========================================================

app.mainloop()