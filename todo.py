import customtkinter as ctk
import tkinter as tk
from PIL import Image
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os
import sys


# =========================================================
# APP SETUP
# =========================================================

app = ctk.CTk()

app.title("Orbit - To Do")
app.attributes("-fullscreen", True)
app.minsize(800, 600)

# ESC closes application
app.bind("<Escape>", lambda event: app.destroy())


# =========================================================
# COLORS
# =========================================================

BACKGROUND = "#071426"
PANEL = "#103764"
CARD = "#0D2038"

BLUE = "#0B3D91"
BLUE_HOVER = "#1261D6"

CYAN = "#35C2FF"

TEXT = "#FFFFFF"
SECONDARY = "#7D91A8"

SCROLLBAR = "#287DB5"
SCROLLBAR_HOVER = "#35C2FF"

DELETE_HOVER = "#7A1F2B"

app.configure(fg_color=BACKGROUND)


# =========================================================
# DATA FILE
# =========================================================

# ---------------------------------------------------------
# RESOURCE PATH
# Works in normal Python and PyInstaller builds.
# ---------------------------------------------------------
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# ---------------------------------------------------------
# USER DATA PATH
# Keep personal task data outside Program Files.
# ---------------------------------------------------------
APP_DATA_DIR = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")),
    "Orbit"
)

os.makedirs(APP_DATA_DIR, exist_ok=True)

DATA_FILE = os.path.join(APP_DATA_DIR, "tasks.json")


# =========================================================
# DEFAULT DATA
# =========================================================

DEFAULT_DATA = {
    "tasks": [],
    "events": []
}


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "events": []}

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        # Protect against old / incomplete JSON

        if "tasks" not in data:
            data["tasks"] = []

        if "events" not in data:
            data["events"] = []

        return data

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {
            "tasks": [],
            "events": []
        }


# =========================================================
# SAVE DATA
# =========================================================

def save_data():

    try:

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError as error:

        print(
            f"Could not save data: {error}"
        )


# =========================================================
# LOAD SAVED DATA
# =========================================================

data = load_data()

tasks = data["tasks"]


# =========================================================
# EVENT LOGGER
# =========================================================

def log_event(
    event_type,
    task_id
):

    event = {

        "type": event_type,

        "task_id": task_id,

        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    data["events"].append(event)

    save_data()


# =========================================================
# GENERATE TASK ID
# =========================================================

def generate_task_id():

    if not tasks:
        return 1

    return max(
        task["id"]
        for task in tasks
    ) + 1


# =========================================================
# BACKGROUND
# =========================================================

BACKGROUND_FILE = resource_path(
    os.path.join("imgs", "todo_bg.png")
)

if not os.path.exists(BACKGROUND_FILE):
    raise FileNotFoundError(
        f"Orbit background image not found: {BACKGROUND_FILE}"
    )

original_image = Image.open(BACKGROUND_FILE)

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
# RESPONSIVE BACKGROUND
# =========================================================

last_width = 0
last_height = 0


def resize_background(event):

    global last_width
    global last_height

    # Only react to main window
    if event.widget != app:
        return

    window_width = event.width
    window_height = event.height

    if (
        window_width <= 0
        or window_height <= 0
    ):
        return

    # Avoid unnecessary processing
    if (
        window_width == last_width
        and window_height == last_height
    ):
        return

    last_width = window_width
    last_height = window_height

    image_width, image_height = (
        original_image.size
    )

    # Maintain aspect ratio
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

    # Keep reference alive
    background_label.bg_image = bg_image


# =========================================================
# TASK ACTIVITY CHART
# =========================================================

activity_frame = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=1,
    border_width=1,
    border_color=SECONDARY
)

activity_frame.place(
    relx=0.05,
    rely=0.09,
    relwidth=0.40,
    relheight=0.38
)

activity_canvas = tk.Canvas(
    activity_frame,
    bg=CARD,
    highlightthickness=0,
    bd=0,
    width=500,
    height=300
)

activity_canvas.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# =========================================================
# TODO CONTAINER
# =========================================================

todo_container = ctk.CTkScrollableFrame(

    app,

    fg_color=PANEL,

    bg_color=PANEL,

    corner_radius=0,

    border_width=1,

    border_color=SECONDARY,

    scrollbar_fg_color=PANEL,

    scrollbar_button_color=SCROLLBAR,

    scrollbar_button_hover_color=SCROLLBAR_HOVER
)

todo_container.place(

    relx=0.52,

    rely=0.03,

    anchor="nw",

    relwidth=0.46,

    relheight=0.94
)



# =========================================================
# REMOVE WHITE CANVAS
# =========================================================

todo_container._parent_canvas.configure(

    bg=PANEL,

    highlightthickness=0,

    borderwidth=0
)


# =========================================================
# TITLE
# =========================================================

title = ctk.CTkLabel(

    todo_container,

    text="MY TASKS",

    font=(
        "Segoe UI",
        32,
        "bold"
    ),

    text_color=TEXT
)

title.pack(
    pady=(30, 20)
)


# =========================================================
# ADD TASK FRAME
# =========================================================

add_task_frame = ctk.CTkFrame(

    todo_container,

    fg_color=CARD,

    corner_radius=12,

    border_width=0
)

add_task_frame.pack(

    fill="x",

    padx=25,

    pady=(0, 20)
)


# =========================================================
# TASK INPUT
# =========================================================

task_entry = ctk.CTkEntry(

    add_task_frame,

    placeholder_text="Enter a new task...",

    height=45,

    font=(
        "Segoe UI",
        16
    ),

    fg_color=BACKGROUND,

    border_color="#1B4F7A",

    border_width=2,

    text_color=TEXT,

    placeholder_text_color=SECONDARY
)

task_entry.pack(

    side="left",

    fill="x",

    expand=True,

    padx=(15, 10),

    pady=15
)


# =========================================================
# ADD BUTTON
# =========================================================

add_button = ctk.CTkButton(

    add_task_frame,

    text="ADD",

    width=90,

    height=45,

    font=(
        "Segoe UI",
        15,
        "bold"
    ),

    fg_color=BLUE,

    hover_color=BLUE_HOVER,

    text_color=TEXT,

    corner_radius=8
)

add_button.pack(

    side="right",

    padx=(0, 15),

    pady=15
)


# =========================================================
# PROGRESS FRAME
# =========================================================

progress_frame = ctk.CTkFrame(

    todo_container,

    fg_color=CARD,

    corner_radius=15,

    border_width=0,

    height=180
)

progress_frame.pack(

    fill="x",

    padx=25,

    pady=(0, 20)
)

progress_frame.pack_propagate(False)


# =========================================================
# PROGRESS TITLE
# =========================================================

progress_title = ctk.CTkLabel(

    progress_frame,

    text="TASK PROGRESS",

    font=(
        "Segoe UI",
        14,
        "bold"
    ),

    text_color=SECONDARY
)

progress_title.place(

    relx=0.05,

    rely=0.18
)


# =========================================================
# TASK COUNT
# =========================================================

task_count_label = ctk.CTkLabel(

    progress_frame,

    text="0 / 0 completed",

    font=(
        "Segoe UI",
        18,
        "bold"
    ),

    text_color=TEXT
)

task_count_label.place(

    relx=0.05,

    rely=0.52
)


# =========================================================
# PROGRESS CANVAS
# =========================================================

progress_canvas = tk.Canvas(

    progress_frame,

    width=110,

    height=110,

    bg=CARD,

    highlightthickness=0,

    bd=0
)

progress_canvas.place(

    relx=0.82,

    rely=0.5,

    anchor="center"
)


# =========================================================
# PROGRESS PERCENTAGE
# =========================================================

progress_text = ctk.CTkLabel(

    progress_frame,

    text="0%",

    font=(
        "Segoe UI",
        26,
        "bold"
    ),

    text_color=TEXT
)

progress_text.place(

    relx=0.82,

    rely=0.5,

    anchor="center"
)


# =========================================================
# TASK SECTION TITLE
# =========================================================

tasks_title = ctk.CTkLabel(

    todo_container,

    text="YOUR TASKS",

    font=(
        "Segoe UI",
        15,
        "bold"
    ),

    text_color=SECONDARY
)

tasks_title.pack(

    anchor="w",

    padx=25,

    pady=(0, 8)
)


# =========================================================
# TASK LIST
# =========================================================

task_list = ctk.CTkFrame(

    todo_container,

    fg_color="transparent",

    border_width=0
)

task_list.pack(

    fill="x",

    padx=25,

    pady=(0, 20)
)


# =========================================================
# WIDGET REFERENCES
# =========================================================

task_widgets = {}


# =========================================================
# GET ACTIVE TASKS
# =========================================================

def get_active_tasks():

    return [

        task

        for task in tasks

        if not task.get(
            "deleted",
            False
        )
    ]


# =========================================================
# UPDATE PROGRESS
# =========================================================

def update_progress():

    active_tasks = get_active_tasks()

    total_tasks = len(
        active_tasks
    )

    completed_tasks = sum(

        1

        for task in active_tasks

        if task.get(
            "completed",
            False
        )
    )

    # Calculate percentage
    if total_tasks == 0:

        percentage = 0

    else:

        percentage = int(

            (
                completed_tasks
                / total_tasks
            ) * 100
        )

    # Clear chart
    progress_canvas.delete(
        "all"
    )

    # Background circle
    progress_canvas.create_oval(

        10,
        10,
        100,
        100,

        outline="#183B60",

        width=10
    )

    # Progress circle
    if percentage > 0:

        progress_canvas.create_arc(

            10,
            10,
            100,
            100,

            start=90,

            extent=(
                -(percentage * 3.6)
            ),

            outline=CYAN,

            width=10,

            style="arc"
        )

    # Percentage
    progress_text.configure(

        text=f"{percentage}%"
    )

    # Count
    task_count_label.configure(

        text=(
            f"{completed_tasks} "
            f"/ "
            f"{total_tasks} "
            f"completed"
        )
    )


# =========================================================
# DRAW TASK ACTIVITY CHART
# =========================================================

def draw_activity_chart():

    activity_canvas.delete("all")

    # -----------------------------------------------------
    # LAST 7 DAYS
    # -----------------------------------------------------

    today = datetime.now().date()

    dates = [
        today - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    # -----------------------------------------------------
    # ACTIVITY DATA
    # -----------------------------------------------------

    added = defaultdict(int)

    completed = defaultdict(int)

    for event in data.get("events", []):

        try:

            event_date = datetime.strptime(
                event["time"],
                "%Y-%m-%d %H:%M:%S"
            ).date()

        except (
            KeyError,
            ValueError
        ):

            continue

        if event_date not in dates:
            continue

        if event["type"] == "task_added":

            added[event_date] += 1

        elif event["type"] == "task_completed":

            completed[event_date] += 1


    # -----------------------------------------------------
    # GET CANVAS SIZE
    # -----------------------------------------------------

    activity_canvas.update_idletasks()

    width = activity_canvas.winfo_width()
    height = activity_canvas.winfo_height()

    if width <= 1:
        width = 500

    if height <= 1:
        height = 300


    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    activity_canvas.create_text(

        25,
        25,

        text="TASK ACTIVITY",

        anchor="w",

        fill=TEXT,

        font=(
            "Segoe UI",
            15,
            "bold"
        )
    )


    # -----------------------------------------------------
    # SUBTITLE
    # -----------------------------------------------------

    activity_canvas.create_text(

        25,
        48,

        text="Last 7 days",

        anchor="w",

        fill=SECONDARY,

        font=(
            "Segoe UI",
            10
        )
    )


    # -----------------------------------------------------
    # CHART AREA
    # -----------------------------------------------------

    left = 55

    right = width - 25

    top = 80

    bottom = height - 55


    # -----------------------------------------------------
    # MAXIMUM VALUE
    # -----------------------------------------------------

    max_value = max(

        [added[d] for d in dates]
        +
        [completed[d] for d in dates]
        +
        [1]
    )


    # -----------------------------------------------------
    # GRID LINES
    # -----------------------------------------------------

    for i in range(4):

        y = (
            bottom
            -
            (
                i
                *
                (
                    bottom - top
                )
                /
                3
            )
        )

        activity_canvas.create_line(

            left,
            y,

            right,
            y,

            fill="#183B60",

            width=1
        )

        value = round(
            max_value * i / 3
        )

        activity_canvas.create_text(

            left - 10,

            y,

            text=str(value),

            anchor="e",

            fill=SECONDARY,

            font=(
                "Segoe UI",
                9
            )
        )


    # -----------------------------------------------------
    # BARS
    # -----------------------------------------------------

    bar_width = 16

    chart_width = right - left

    day_spacing = (
        chart_width / len(dates)
    )


    for index, date in enumerate(dates):

        center_x = (
            left
            +
            day_spacing * index
            +
            day_spacing / 2
        )


        # ---------------------------------------------
        # ADDED
        # ---------------------------------------------

        added_value = added[date]

        added_height = (

            0

            if max_value == 0

            else
            (
                added_value
                /
                max_value
            )
            *
            (
                bottom - top
            )
        )

        activity_canvas.create_rectangle(

            center_x - bar_width - 2,

            bottom - added_height,

            center_x - 2,

            bottom,

            fill=BLUE,

            outline=""
        )


        # ---------------------------------------------
        # COMPLETED
        # ---------------------------------------------

        completed_value = completed[date]

        completed_height = (

            0

            if max_value == 0

            else
            (
                completed_value
                /
                max_value
            )
            *
            (
                bottom - top
            )
        )

        activity_canvas.create_rectangle(

            center_x + 2,

            bottom - completed_height,

            center_x + bar_width + 2,

            bottom,

            fill=CYAN,

            outline=""
        )


        # ---------------------------------------------
        # DAY LABEL
        # ---------------------------------------------

        activity_canvas.create_text(

            center_x,

            bottom + 18,

            text=date.strftime("%a"),

            fill=SECONDARY,

            font=(
                "Segoe UI",
                9
            )
        )


    # -----------------------------------------------------
    # LEGEND
    # -----------------------------------------------------

    legend_y = height - 20


    # Added

    activity_canvas.create_rectangle(

        25,
        legend_y - 5,

        35,
        legend_y + 5,

        fill=BLUE,

        outline=""
    )

    activity_canvas.create_text(

        42,
        legend_y,

        text="Added",

        anchor="w",

        fill=SECONDARY,

        font=(
            "Segoe UI",
            9
        )
    )


    # Completed

    activity_canvas.create_rectangle(

        100,
        legend_y - 5,

        110,
        legend_y + 5,

        fill=CYAN,

        outline=""
    )

    activity_canvas.create_text(

        117,
        legend_y,

        text="Completed",

        anchor="w",

        fill=SECONDARY,

        font=(
            "Segoe UI",
            9
        )
    )


# =========================================================
# TOGGLE TASK
# =========================================================

def toggle_task(
    task,
    checkbox
):

    is_completed = (
        checkbox.get() == 1
    )

    previous_state = task.get(
        "completed",
        False
    )


    # -----------------------------------------
    # CHECKED
    # -----------------------------------------

    if is_completed:

        task["completed"] = True

        # Only log if it changed
        if not previous_state:

            task["completed_at"] = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            log_event(
                "task_completed",
                task["id"]
            )


    # -----------------------------------------
    # UNCHECKED
    # -----------------------------------------

    else:

        task["completed"] = False

        task["completed_at"] = None

        # Only log if it was previously completed
        if previous_state:

            log_event(
                "task_uncompleted",
                task["id"]
            )


    # Save latest state
    save_data()

    # Update progress
    update_progress()

    refresh_insights()

    # Update activity chart
    draw_activity_chart()


# =========================================================
# DELETE TASK
# =========================================================

def delete_task(
    task,
    task_frame
):

    # Mark deleted instead of
    # permanently removing it.
    task["deleted"] = True

    task["deleted_at"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    # Record event
    log_event(
        "task_deleted",
        task["id"]
    )


    # Remove widget
    task_frame.destroy()


    # Remove widget reference
    task_widgets.pop(
        task["id"],
        None
    )


    # Save
    save_data()


    # Update progress
    update_progress()

    # Update activity chart
    draw_activity_chart()

    # Update insights
    refresh_insights()


# =========================================================
# CREATE TASK WIDGET
# =========================================================

def create_task_widget(task):

    task_frame = ctk.CTkFrame(

        task_list,

        height=60,

        fg_color=CARD,

        corner_radius=10,

        border_width=0
    )

    task_frame.pack(

        fill="x",

        pady=6
    )

    task_frame.pack_propagate(
        False
    )


    # =====================================================
    # CHECKBOX
    # =====================================================

    checkbox = ctk.CTkCheckBox(

        task_frame,

        text=task["text"],

        font=(
            "Segoe UI",
            16
        ),

        text_color=TEXT,

        fg_color=BLUE,

        hover_color=BLUE_HOVER,

        border_color=CYAN,

        checkbox_width=22,

        checkbox_height=22,

        command=lambda:
            toggle_task(
                task,
                checkbox
            )
    )

    checkbox.pack(

        side="left",

        fill="x",

        expand=True,

        padx=20
    )


    # Restore state
    if task.get(
        "completed",
        False
    ):

        checkbox.select()


    # =====================================================
    # DELETE BUTTON
    # =====================================================

    delete_button = ctk.CTkButton(

        task_frame,

        text="✕",

        width=35,

        height=35,

        font=(
            "Segoe UI",
            14,
            "bold"
        ),

        fg_color="transparent",

        hover_color=DELETE_HOVER,

        text_color=TEXT,

        corner_radius=8,

        command=lambda:
            delete_task(
                task,
                task_frame
            )
    )

    delete_button.pack(

        side="right",

        padx=10
    )


    # Store references
    task_widgets[
        task["id"]
    ] = {

        "frame": task_frame,

        "checkbox": checkbox
    }


# =========================================================
# REFRESH TASK LIST
# =========================================================

def refresh_tasks():

    # Remove existing widgets
    for widget in task_list.winfo_children():

        widget.destroy()

    task_widgets.clear()


    # Recreate active tasks
    for task in tasks:

        if task.get(
            "deleted",
            False
        ):

            continue

        create_task_widget(
            task
        )


    # Update progress
    update_progress()


    # Update insights
    refresh_insights()


# =========================================================
# ADD TASK
# =========================================================

def add_task():

    task_text = (
        task_entry.get().strip()
    )


    # Don't allow empty tasks
    if not task_text:

        return


    # Create task
    new_task = {

        "id": generate_task_id(),

        "text": task_text,

        "created_at": (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ),

        "completed": False,

        "completed_at": None,

        "deleted": False,

        "deleted_at": None
    }


    # Add task
    tasks.append(
        new_task
    )


    # Record event
    log_event(
        "task_added",
        new_task["id"]
    )


    # Save
    save_data()


    # Add to UI
    create_task_widget(
        new_task
    )


    # Update progress
    update_progress()

    # Update activity chart
    draw_activity_chart()


    # Update insights
    refresh_insights()


    # Clear input
    task_entry.delete(
        0,
        "end"
    )


    # Focus input
    task_entry.focus()

# =========================================================
# bottom frame
# =========================================================

bottom_frame = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=1,
    border_width=1,
    border_color=SECONDARY
)

bottom_frame.place(
    relx=0.05,
    rely=0.53,
    relwidth=0.40,
    relheight=0.38
)

# =========================================================
# TASK INSIGHTS
# =========================================================

insight_title = ctk.CTkLabel(
    bottom_frame,
    text="TASK INSIGHTS",
    font=("Segoe UI", 18, "bold"),
    text_color=TEXT
)

insight_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 2)
)


insight_subtitle = ctk.CTkLabel(
    bottom_frame,
    text="Overview of your current productivity",
    font=("Segoe UI", 11),
    text_color=SECONDARY
)

insight_subtitle.pack(
    anchor="w",
    padx=25,
    pady=(0, 15)
)


# =========================================================
# INSIGHT DATA
# =========================================================

def refresh_insights():

    active_tasks = [
        task for task in tasks
        if not task.get("deleted", False)
    ]

    total_tasks = len(active_tasks)

    completed_tasks = sum(
        1 for task in active_tasks
        if task.get("completed", False)
    )

    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        completion_rate = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        completion_rate = 0

    # -----------------------------------------
    # UPDATE VALUES
    # -----------------------------------------

    total_value.configure(
        text=str(total_tasks)
    )

    completed_value.configure(
        text=str(completed_tasks)
    )

    pending_value.configure(
        text=str(pending_tasks)
    )

    rate_value.configure(
        text=f"{completion_rate}%"
    )


# =========================================================
# INSIGHT CARDS CONTAINER
# =========================================================

insight_cards = ctk.CTkFrame(
    bottom_frame,
    fg_color="transparent"
)

insight_cards.pack(
    fill="x",
    padx=20,
    pady=(0, 15)
)


# =========================================================
# TOTAL TASKS
# =========================================================

total_card = ctk.CTkFrame(
    insight_cards,
    fg_color=BACKGROUND,
    corner_radius=10
)

total_card.grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="nsew"
)


ctk.CTkLabel(
    total_card,
    text="TOTAL",
    font=("Segoe UI", 10, "bold"),
    text_color=SECONDARY
).pack(
    pady=(10, 0)
)


total_value = ctk.CTkLabel(
    total_card,
    text="0",
    font=("Segoe UI", 22, "bold"),
    text_color=TEXT
)

total_value.pack(
    pady=(0, 10)
)


# =========================================================
# COMPLETED
# =========================================================

completed_card = ctk.CTkFrame(
    insight_cards,
    fg_color=BACKGROUND,
    corner_radius=10
)

completed_card.grid(
    row=0,
    column=1,
    padx=5,
    pady=5,
    sticky="nsew"
)


ctk.CTkLabel(
    completed_card,
    text="COMPLETED",
    font=("Segoe UI", 10, "bold"),
    text_color=SECONDARY
).pack(
    pady=(10, 0)
)


completed_value = ctk.CTkLabel(
    completed_card,
    text="0",
    font=("Segoe UI", 22, "bold"),
    text_color=CYAN
)

completed_value.pack(
    pady=(0, 10)
)


# =========================================================
# PENDING
# =========================================================

pending_card = ctk.CTkFrame(
    insight_cards,
    fg_color=BACKGROUND,
    corner_radius=10
)

pending_card.grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="nsew"
)


ctk.CTkLabel(
    pending_card,
    text="PENDING",
    font=("Segoe UI", 10, "bold"),
    text_color=SECONDARY
).pack(
    pady=(10, 0)
)


pending_value = ctk.CTkLabel(
    pending_card,
    text="0",
    font=("Segoe UI", 22, "bold"),
    text_color=TEXT
)

pending_value.pack(
    pady=(0, 10)
)


# =========================================================
# COMPLETION RATE
# =========================================================

rate_card = ctk.CTkFrame(
    insight_cards,
    fg_color=BACKGROUND,
    corner_radius=10
)

rate_card.grid(
    row=1,
    column=1,
    padx=5,
    pady=5,
    sticky="nsew"
)


ctk.CTkLabel(
    rate_card,
    text="COMPLETION",
    font=("Segoe UI", 10, "bold"),
    text_color=SECONDARY
).pack(
    pady=(10, 0)
)


rate_value = ctk.CTkLabel(
    rate_card,
    text="0%",
    font=("Segoe UI", 22, "bold"),
    text_color=CYAN
)

rate_value.pack(
    pady=(0, 10)
)


# Make the four cards resize evenly
insight_cards.grid_columnconfigure(0, weight=1)
insight_cards.grid_columnconfigure(1, weight=1)


# =========================================================
# PRODUCTIVITY MESSAGE
# =========================================================

insight_message = ctk.CTkLabel(
    bottom_frame,
    text="Keep going — every completed task counts.",
    font=("Segoe UI", 11),
    text_color=SECONDARY
)

insight_message.pack(
    anchor="w",
    padx=25,
    pady=(0, 10)
)


# =========================================================
# INITIAL UPDATE
# =========================================================

refresh_insights()


# =========================================================
# ADD BUTTON
# =========================================================

add_button.configure(

    command=add_task
)


# =========================================================
# ENTER KEY
# =========================================================

task_entry.bind(

    "<Return>",

    lambda event:
        add_task()
)



# =========================================================
# LOAD SAVED TASKS
# =========================================================

refresh_tasks()

# Wait until the entire UI has been created
# and then draw the chart.
app.after(100, draw_activity_chart)


# =========================================================
# ACTIVITY CHART RESIZE
# =========================================================

def redraw_activity_chart(event=None):
    draw_activity_chart()


activity_canvas.bind(
    "<Configure>",
    redraw_activity_chart
)


# =========================================================
# WINDOW RESIZE
# =========================================================

app.bind(

    "<Configure>",

    resize_background
)


# =========================================================
# START APP
# =========================================================

app.mainloop()