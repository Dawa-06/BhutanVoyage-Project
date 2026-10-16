
import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import os
import re

# ==========================================
# 1. MAIN WINDOW
# ==========================================
root = tk.Tk()
root.title("BhutanVoyage - Create Traveller Account")
root.state("zoomed")
root.minsize(700, 600)
root.configure(bg="#EEEAE0")

# ==========================================
# 2. COLOURS
# ==========================================
WHITE = "#FFFFFF"
MAROON = "#7B241C"
DARK_MAROON = "#5C1A14"
TEXT_DARK = "#2C3E50"
TEXT_LIGHT = "#7F8C8D"
MAIN_BG = "#EEEAE0"
ERROR_RED = "#C0392B"

# ==========================================
# 3. FONTS
# ==========================================
font_title = font.Font(
    family="Georgia", size=22, weight="bold"
)

# ==========================================
# 4. SCROLLABLE MAIN AREA
# ==========================================
main_area = tk.Frame(root, bg=MAIN_BG)
main_area.pack(fill="both", expand=True)

canvas = tk.Canvas(
    main_area,
    bg=MAIN_BG,
    highlightthickness=0
)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(
    main_area,
    orient="vertical",
    command=canvas.yview
)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas, bg=MAIN_BG)

window_id = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind(
    "<Configure>",
    update_scroll_region
)

def resize_content(event):
    canvas.itemconfigure(window_id, width=event.width)

canvas.bind("<Configure>", resize_content)

# Mouse-wheel scrolling
def on_mousewheel(event):
    if event.delta:
        canvas.yview_scroll(
            -int(event.delta / 120),
            "units"
        )

canvas.bind_all("<MouseWheel>", on_mousewheel)

# ==========================================
# 5. REGISTRATION FORM CARD
# ==========================================
form_card = tk.Frame(
    scrollable_frame,
    bg=WHITE,
    width=540,
    height=650,
    highlightbackground="#E5E0D8",
    highlightthickness=1
)
form_card.pack(pady=30)
form_card.pack_propagate(False)

# Close button
tk.Button(
    form_card,
    text="✖ CLOSE",
    font=("Helvetica", 8, "bold"),
    bg=WHITE,
    fg=TEXT_LIGHT,
    relief="flat",
    cursor="hand2",
    command=root.destroy
).place(relx=0.95, y=18, anchor="ne")

# Account heading
tk.Label(
    form_card,
    text="TRAVELLER ACCOUNT",
    font=("Helvetica", 9, "bold"),
    fg=MAROON,
    bg=WHITE
).pack(pady=(42, 7))

tk.Label(
    form_card,
    text="Create Account",
    font=font_title,
    fg="#111111",
    bg=WHITE
).pack()

tk.Label(
    form_card,
    text="Join BhutanVoyage and start planning your dream Bhutan adventure!",
    font=("Helvetica", 9),
    fg="#222222",
    bg=WHITE,
    wraplength=450
).pack(pady=(12, 18))

# ==========================================
# 6. INPUT FIELDS AND ERROR LABELS
# ==========================================
fields_frame = tk.Frame(form_card, bg=WHITE)
fields_frame.pack(fill="x", padx=65)

def create_field(label_text, show=None):
    tk.Label(
        fields_frame,
        text=label_text,
        font=("Helvetica", 9, "bold"),
        fg="#555555",
        bg=WHITE
    ).pack(anchor="w", pady=(2, 2))

    entry = tk.Entry(
        fields_frame,
        font=("Helvetica", 11),
        relief="solid",
        bd=1,
        show=show
    )
    entry.pack(fill="x", ipady=3, pady=(0, 5))

    error_label = tk.Label(
        fields_frame,
        text="",
        font=("Helvetica", 8),
        fg=ERROR_RED,
        bg=WHITE
    )
    error_label.pack(anchor="w")

    return entry, error_label

name_entry, name_error = create_field("Full Name")
email_entry, email_error = create_field("Email Address")
password_entry, password_error = create_field(
    "Password", show="*"
)
confirm_entry, confirm_error = create_field(
    "Confirm Password", show="*"
)

# ==========================================
# 7. TERMS AND CONDITIONS
# ==========================================
agree_var = tk.BooleanVar(value=False)

tk.Checkbutton(
    form_card,
    text="I agree to the Terms of Service and Privacy Policy",
    variable=agree_var,
    font=("Helvetica", 9),
    fg=TEXT_DARK,
    bg=WHITE,
    activebackground=WHITE,
    selectcolor=WHITE,
    cursor="hand2"
).pack(pady=(3, 5))

terms_error = tk.Label(
    form_card,
    text="",
    font=("Helvetica", 8),
    fg=ERROR_RED,
    bg=WHITE
)
terms_error.pack()

# ==========================================
# 8. VALIDATION FUNCTION
# ==========================================
def create_account():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_entry.get()

    # Clear previous errors
    name_error.config(text="")
    email_error.config(text="")
    password_error.config(text="")
    confirm_error.config(text="")
    terms_error.config(text="")

    valid = True

    # Full name validation
    if not name:
        name_error.config(
            text="Please enter your full name."
        )
        valid = False

    # Email validation
    if not email:
        email_error.config(
            text="Please enter your email address."
        )
        valid = False
    elif not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email
    ):
        email_error.config(
            text="Please enter a valid email address."
        )
        valid = False

    # Password validation
    if not password:
        password_error.config(
            text="Please enter a password."
        )
        valid = False
    elif len(password) < 6:
        password_error.config(
            text="Password must contain at least 6 characters."
        )
        valid = False

    # Confirm password validation
    if not confirm_password:
        confirm_error.config(
            text="Please confirm your password."
        )
        valid = False
    elif password and password != confirm_password:
        confirm_error.config(
            text="Passwords do not match."
        )
        valid = False

    # Terms validation
    if not agree_var.get():
        terms_error.config(
            text="Please agree to the Terms and Privacy Policy."
        )
        valid = False

    if not valid:
        return

    messagebox.showinfo(
        "Account Created",
        f"Welcome to BhutanVoyage, {name}!"
    )

# ==========================================
# 9. CREATE ACCOUNT BUTTON
# ==========================================
tk.Button(
    form_card,
    text="Create Account     ✓",
    font=("Helvetica", 10, "bold"),
    bg=MAROON,
    fg=WHITE,
    activebackground=DARK_MAROON,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=create_account
).pack(fill="x", padx=65, ipady=5, pady=(5, 0))

# ==========================================
# 10. LOGIN LINK
# ==========================================
login_frame = tk.Frame(form_card, bg=WHITE)
login_frame.pack(pady=8)

tk.Label(
    login_frame,
    text="Already have an account?",
    font=("Helvetica", 9),
    fg=TEXT_LIGHT,
    bg=WHITE
).pack(side="left", padx=3)

tk.Button(
    login_frame,
    text="Login here",
    font=("Helvetica", 9, "bold"),
    fg=MAROON,
    bg=WHITE,
    relief="flat",
    cursor="hand2",
    command=lambda: messagebox.showinfo(
        "Login",
        "Connect this button to your login page."
    )
).pack(side="left")

# Close registration button
tk.Button(
    form_card,
    text="← CLOSE REGISTRATION",
    font=("Helvetica", 8),
    fg=TEXT_LIGHT,
    bg=WHITE,
    relief="flat",
    cursor="hand2",
    command=root.destroy
).place(relx=0.5, y=620, anchor="center")

# ==========================================
# 11. RUN APPLICATION
# ==========================================
root.mainloop()
