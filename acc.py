import customtkinter as ctk
from PIL import Image
import json
import subprocess
import sys
import os
import re
from datetime import datetime, date


# =========================================================
# CUSTOMTKINTER SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# APP
# =========================================================

app = ctk.CTk()

app.title("Orbit - Account Details")
app.geometry("1000x700")
app.resizable(True, True)

app.bind(
    "<Escape>",
    lambda e: app.destroy()
)


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
ERROR = "#FF6B6B"


# =========================================================
# RESOURCE PATH
# =========================================================

def resource_path(relative_path):
    """
    Returns the correct path for:

    1. Normal Python execution
    2. PyInstaller executable
    """

    if getattr(sys, "frozen", False):

        base_path = sys._MEIPASS

    else:

        base_path = os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.join(
        base_path,
        relative_path
    )


# =========================================================
# APPLICATION DATA DIRECTORY
# =========================================================

APP_DATA_DIR = os.path.join(
    os.environ.get(
        "APPDATA",
        os.path.expanduser("~")
    ),
    "Orbit"
)

os.makedirs(
    APP_DATA_DIR,
    exist_ok=True
)


# =========================================================
# PROFILE FILE
# =========================================================

PROFILE_FILE = os.path.join(
    APP_DATA_DIR,
    "profile.json"
)


# =========================================================
# TODO APPLICATION
# =========================================================

# Development version
TODO_FILE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "todo.py"
)

# Installed / PyInstaller version
INSTALL_DIR = os.path.dirname(
    sys.executable
)

TODO_EXE = os.path.join(
    INSTALL_DIR,
    "OrbitTodo",
    "OrbitTodo.exe"
)

# =========================================================
# BACKGROUND
# =========================================================

BACKGROUND_IMAGE = resource_path(
    os.path.join(
        "imgs",
        "acc.png"
    )
)


try:

    bg_image = ctk.CTkImage(
        light_image=Image.open(
            BACKGROUND_IMAGE
        ),
        dark_image=Image.open(
            BACKGROUND_IMAGE
        ),
        size=(1000, 700)
    )

except Exception as error:

    print(
        f"Could not load background image: {error}"
    )

    bg_image = None


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
    font=(
        "Segoe UI",
        25,
        "bold"
    ),
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
    font=(
        "Segoe UI",
        13
    ),
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
    font=(
        "Segoe UI",
        15
    ),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

name_entry.pack(
    pady=6
)


# =========================================================
# DATE OF BIRTH
# =========================================================

dob_entry = ctk.CTkEntry(
    card,
    placeholder_text="Date of Birth (DD-MM-YYYY)",
    width=400,
    height=45,
    font=(
        "Segoe UI",
        15
    ),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

dob_entry.pack(
    pady=6
)


# =========================================================
# EMAIL
# =========================================================

email_entry = ctk.CTkEntry(
    card,
    placeholder_text="Email Address",
    width=400,
    height=45,
    font=(
        "Segoe UI",
        15
    ),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

email_entry.pack(
    pady=6
)


# =========================================================
# USERNAME
# =========================================================

username_entry = ctk.CTkEntry(
    card,
    placeholder_text="Username",
    width=400,
    height=45,
    font=(
        "Segoe UI",
        15
    ),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

username_entry.pack(
    pady=6
)


# =========================================================
# PHONE
# =========================================================

phone_entry = ctk.CTkEntry(
    card,
    placeholder_text="Phone Number (Optional)",
    width=400,
    height=45,
    font=(
        "Segoe UI",
        15
    ),
    fg_color=BACKGROUND,
    border_color=BORDER,
    border_width=2,
    text_color=TEXT,
    placeholder_text_color=SECONDARY
)

phone_entry.pack(
    pady=6
)


# =========================================================
# STATUS MESSAGE
# =========================================================

status_label = ctk.CTkLabel(
    card,
    text="",
    font=(
        "Segoe UI",
        12
    ),
    text_color=CYAN
)

status_label.pack(
    pady=(5, 5)
)


# =========================================================
# VALIDATION FUNCTIONS
# =========================================================

def validate_name(name):

    # Allow letters and spaces
    pattern = r"^[A-Za-z][A-Za-z .'-]{1,49}$"

    return bool(
        re.fullmatch(
            pattern,
            name
        )
    )


# ---------------------------------------------------------
# DATE OF BIRTH + AGE
# ---------------------------------------------------------

def validate_dob(dob):

    try:

        # Check format and create date
        birth_date = datetime.strptime(
            dob,
            "%d-%m-%Y"
        ).date()

    except ValueError:

        return False, "Use DOB format: DD-MM-YYYY."

    today = date.today()

    # Future DOB
    if birth_date > today:

        return False, "Date of birth cannot be in the future."

    # Very old DOB
    if birth_date.year < 1900:

        return False, "Please enter a valid date of birth."

    # Calculate age
    age = (
        today.year
        - birth_date.year
        - (
            (today.month, today.day)
            < (birth_date.month, birth_date.day)
        )
    )

    # Minimum age
    if age < 13:

        return False, "You must be at least 13 years old."

    # Unrealistic age
    if age > 120:

        return False, "Please enter a valid date of birth."

    return True, age


# ---------------------------------------------------------
# EMAIL
# ---------------------------------------------------------

def validate_email(email):

    pattern = (
        r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@"
        r"[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
        r"(?:\.[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
    )

    return bool(
        re.fullmatch(
            pattern,
            email
        )
    )


# ---------------------------------------------------------
# PHONE
# ---------------------------------------------------------

def validate_phone(phone):

    if not phone:
        return True

    # Remove spaces, hyphens and brackets
    cleaned_phone = re.sub(
        r"[\s()-]",
        "",
        phone
    )

    # Indian number:
    # 9876543210
    # +919876543210
    # 919876543210
    pattern = r"^(?:\+91|91)?[6-9]\d{9}$"

    return bool(
        re.fullmatch(
            pattern,
            cleaned_phone
        )
    )


# ---------------------------------------------------------
# USERNAME
# ---------------------------------------------------------

def validate_username(username):

    # 3-20 characters
    # Letters, numbers and underscore
    pattern = r"^[A-Za-z0-9_]{3,20}$"

    return bool(
        re.fullmatch(
            pattern,
            username
        )
    )


# =========================================================
# OPEN TODO APPLICATION
# =========================================================

def open_todo():

    try:

        # =========================================
        # PYINSTALLER VERSION
        # =========================================

        if getattr(
            sys,
            "frozen",
            False
        ):

            if not os.path.exists(
                TODO_EXE
            ):

                status_label.configure(
                    text="Orbit Tasks application not found.",
                    text_color=ERROR
                )

                print(
                    "OrbitTodo.exe not found:"
                )

                print(
                    TODO_EXE
                )

                return

            subprocess.Popen(
                [TODO_EXE],
                cwd=os.path.dirname(
                    TODO_EXE
                )
            )


        # =========================================
        # DEVELOPMENT VERSION
        # =========================================

        else:

            if not os.path.exists(
                TODO_FILE
            ):

                status_label.configure(
                    text="todo.py was not found.",
                    text_color=ERROR
                )

                return

            subprocess.Popen(
                [
                    sys.executable,
                    TODO_FILE
                ],
                cwd=os.path.dirname(
                    TODO_FILE
                )
            )


        # Close account window
        app.destroy()


    except Exception as error:

        status_label.configure(
            text="Could not open Orbit Tasks.",
            text_color=ERROR
        )

        print(
            f"Could not launch todo application: {error}"
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


    # =========================================
    # VALIDATE NAME
    # =========================================

    if not name:

        status_label.configure(
            text="Please enter your name.",
            text_color=ERROR
        )

        name_entry.focus()

        return


    if not validate_name(name):

        status_label.configure(
            text="Please enter a valid name.",
            text_color=ERROR
        )

        name_entry.focus()

        return


    # =========================================
    # VALIDATE DOB
    # =========================================

    if not dob:

        status_label.configure(
            text="Please enter your date of birth.",
            text_color=ERROR
        )

        dob_entry.focus()

        return


    dob_valid, age_result = validate_dob(dob)

    if not dob_valid:

        status_label.configure(
            text=age_result,
            text_color=ERROR
        )

        dob_entry.focus()

        return


    age = age_result


    # =========================================
    # VALIDATE EMAIL
    # =========================================

    if not email:

        status_label.configure(
            text="Please enter your email.",
            text_color=ERROR
        )

        email_entry.focus()

        return


    if not validate_email(email):

        status_label.configure(
            text="Please enter a valid email address.",
            text_color=ERROR
        )

        email_entry.focus()

        return


    # =========================================
    # VALIDATE USERNAME
    # =========================================

    if not username:

        status_label.configure(
            text="Please enter a username.",
            text_color=ERROR
        )

        username_entry.focus()

        return


    if not validate_username(username):

        status_label.configure(
            text="Username must be 3-20 characters.",
            text_color=ERROR
        )

        username_entry.focus()

        return


    # =========================================
    # VALIDATE PHONE
    # =========================================

    if phone:

        if not validate_phone(phone):

            status_label.configure(
                text="Enter a valid Indian phone number.",
                text_color=ERROR
            )

            phone_entry.focus()

            return


    # =========================================
    # CREATE PROFILE
    # =========================================

    profile = {

        "name": name,

        "dob": dob,

        "age": age,

        "email": email,

        "username": username,

        "phone": phone

    }


    # =========================================
    # SAVE PROFILE
    # =========================================

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


        # =====================================
        # SUCCESS
        # =====================================

        status_label.configure(
            text="✓ Profile saved successfully!",
            text_color=CYAN
        )


        # =====================================
        # OPEN TODO
        # =====================================

        app.after(
            300,
            open_todo
        )


    except OSError as error:

        status_label.configure(
            text="Could not save profile.",
            text_color=ERROR
        )

        print(
            f"Profile save error: {error}"
        )


# =========================================================
# CREATE PROFILE BUTTON
# =========================================================

save_button = ctk.CTkButton(
    card,
    text="CREATE PROFILE",
    width=400,
    height=45,
    font=(
        "Segoe UI",
        15,
        "bold"
    ),
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
# FOCUS NAME ENTRY
# =========================================================

name_entry.focus()


# =========================================================
# START APPLICATION
# =========================================================

app.mainloop()
