
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
root.minsize(900, 650)
root.configure(bg="#FFFFFF")

# ==========================================
# 2. COLOURS
# ==========================================
WHITE = "#FFFFFF"
MAROON = "#7B241C"
DARK_MAROON = "#5C1A14"
TEXT_DARK = "#2C3E50"
TEXT_LIGHT = "#7F8C8D"
FOOTER_SOFT = "#E6B0AA"
FOOTER_ADMIN = "#F5DEB3"
MAIN_BG = "#EEEAE0"
ERROR_RED = "#C0392B"

# ==========================================
# 3. FONTS
# ==========================================
font_logo = font.Font(family="Helvetica", size=18, weight="bold")
font_nav = font.Font(family="Georgia", size=12)
font_button = font.Font(family="Georgia", size=11, weight="bold")
font_title = font.Font(family="Georgia", size=22, weight="bold")
font_footer_brand = font.Font(family="Georgia", size=15, weight="bold")
font_footer_sub = font.Font(family="Georgia", size=10, slant="italic")
font_footer_tag = font.Font(family="Helvetica", size=10)
font_footer_admin = font.Font(family="Helvetica", size=10, weight="bold")

# ==========================================
# 4. HEADER
# ==========================================
header = tk.Frame(root, bg=WHITE, height=90)
header.pack(side="top", fill="x")
header.pack_propagate(False)

header.columnconfigure(0, weight=0)
header.columnconfigure(1, weight=1)
header.columnconfigure(2, weight=0)

# Logo
logo_path = os.path.join("images", "logo.jpg")

if os.path.exists(logo_path):
    original_logo = Image.open(logo_path).convert("RGBA")
    original_logo.thumbnail((60, 60), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(original_logo)

    logo_label = tk.Label(header, image=logo_photo, bg=WHITE)
    logo_label.image = logo_photo
    logo_label.grid(row=0, column=0, padx=30, pady=15, sticky="w")
else:
    tk.Label(
        header,
        text="BhutanVoyage",
        font=font_logo,
        fg=MAROON,
        bg=WHITE
    ).grid(row=0, column=0, padx=30, pady=15, sticky="w")

    print("Logo not found. Put logo.jpg inside the images folder.")

# Navigation links
nav_frame = tk.Frame(header, bg=WHITE)
nav_frame.grid(row=0, column=1, sticky="ew")

nav_inner = tk.Frame(nav_frame, bg=WHITE)
nav_inner.pack(expand=True)

for item in ["Home", "Destination", "Booking", "About us"]:
    tk.Label(
        nav_inner,
        text=item,
        font=font_nav,
        fg=MAROON,
        bg=WHITE,
        cursor="hand2"
    ).pack(side="left", padx=25)

# Plan Your Trip button
tk.Button(
    header,
    text="Plan Your Trip",
    bg=MAROON,
    fg=WHITE,
    font=font_button,
    relief="flat",
    padx=22,
    pady=10,
    cursor="hand2",
    activebackground=DARK_MAROON,
    activeforeground=WHITE
).grid(row=0, column=2, padx=30, pady=15, sticky="e")

# ==========================================
# 5. SCROLLABLE MAIN AREA
# ==========================================
main_area = tk.Frame(root, bg=MAIN_BG)
main_area.pack(fill="both", expand=True)

# Canvas
canvas = tk.Canvas(
    main_area,
    bg=MAIN_BG,
    highlightthickness=0
)
canvas.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(
    main_area,
    orient="vertical",
    command=canvas.yview
)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Frame inside the canvas
scrollable_frame = tk.Frame(canvas, bg=MAIN_BG)

window_id = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

# Update scrolling region
def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scroll_region)

# Make content fit the canvas width
def resize_content(event):
    canvas.itemconfigure(window_id, width=event.width)

canvas.bind("<Configure>", resize_content)

# Mouse-wheel scrolling
def on_mousewheel(event):
    if event.delta:
        canvas.yview_scroll(-int(event.delta / 120), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

# Linux mouse-wheel support
canvas.bind_all(
    "<Button-4>",
    lambda event: canvas.yview_scroll(-1, "units")
)
canvas.bind_all(
    "<Button-5>",
    lambda event: canvas.yview_scroll(1, "units")
)

# ==========================================
# 6. REGISTRATION FORM CARD
# ==========================================
form_card = tk.Frame(
    scrollable_frame,
    bg=WHITE,
    width=540,
    height=650,
    highlightbackground="#E5E0D8",
    highlightthickness=1
)

form_card.pack(pady=25)
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
# 7. INPUT FIELDS AND ERROR LABELS
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
password_entry, password_error = create_field("Password", show="*")
confirm_entry, confirm_error = create_field("Confirm Password", show="*")

# ==========================================
# 8. TERMS AND CONDITIONS
# ==========================================
agree_var = tk.BooleanVar(value=False)

agree_checkbox = tk.Checkbutton(
    form_card,
    text="I agree to the Terms of Service and Privacy Policy",
    variable=agree_var,
    font=("Helvetica", 9),
    fg=TEXT_DARK,
    bg=WHITE,
    activebackground=WHITE,
    selectcolor=WHITE,
    cursor="hand2"
)
agree_checkbox.pack(pady=(3, 8))

terms_error = tk.Label(
    form_card,
    text="",
    font=("Helvetica", 8),
    fg=ERROR_RED,
    bg=WHITE
)
terms_error.pack()

# ==========================================
# 9. VALIDATION FUNCTION
# ==========================================
def create_account():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_entry.get()

    # Clear previous error messages
    name_error.config(text="")
    email_error.config(text="")
    password_error.config(text="")
    confirm_error.config(text="")
    terms_error.config(text="")

    valid = True

    # Name validation
    if not name:
        name_error.config(text="Please enter your full name.")
        valid = False

    # Email validation
    if not email:
        email_error.config(text="Please enter your email address.")
        valid = False
    elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        email_error.config(text="Please enter a valid email address.")
        valid = False

    # Password validation
    if not password:
        password_error.config(text="Please enter a password.")
        valid = False
    elif len(password) < 6:
        password_error.config(
            text="Password must contain at least 6 characters."
        )
        valid = False

    # Confirm password validation
    if not confirm_password:
        confirm_error.config(text="Please confirm your password.")
        valid = False
    elif password and password != confirm_password:
        confirm_error.config(text="Passwords do not match.")
        valid = False

    # Terms validation
    if not agree_var.get():
        terms_error.config(
            text="Please agree to the Terms and Privacy Policy."
        )
        valid = False

    if not valid:
        canvas.yview_moveto(0)
        return

    messagebox.showinfo(
        "Account Created",
        f"Welcome to BhutanVoyage, {name}!"
    )

# ==========================================
# 10. CREATE ACCOUNT BUTTON
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
).pack(fill="x", padx=65, ipady=5)

# ==========================================
# 11. LOGIN LINK
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

# Close registration link
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
# 12. FOOTER
# ==========================================
footer = tk.Frame(root, bg=MAROON, height=80)
footer.pack(side="bottom", fill="x")
footer.pack_propagate(False)

footer.columnconfigure(0, weight=0)
footer.columnconfigure(1, weight=1)
footer.columnconfigure(2, weight=0)

# Left: Brand and slogan
brand_frame = tk.Frame(footer, bg=MAROON)
brand_frame.grid(row=0, column=0, sticky="w", padx=40, pady=12)

tk.Label(
    brand_frame,
    text="BhutanVoyage",
    font=font_footer_brand,
    bg=MAROON,
    fg=WHITE
).pack(anchor="w")

tk.Label(
    brand_frame,
    text="Plan Himalayan Dreams, Always.",
    font=font_footer_sub,
    bg=MAROON,
    fg=FOOTER_SOFT
).pack(anchor="w")

# Centre: Tagline
tk.Label(
    footer,
    text="Made for curious people",
    font=font_footer_tag,
    bg=MAROON,
    fg=FOOTER_SOFT
).grid(row=0, column=1)

# Right: Admin Login
tk.Button(
    footer,
    text="Admin Login",
    font=font_footer_admin,
    bg=MAROON,
    fg=FOOTER_ADMIN,
    activebackground=MAROON,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=lambda: messagebox.showinfo(
        "Admin Login",
        "Connect this button to the admin login page."
    )
).grid(row=0, column=2, sticky="e", padx=40)

# ==========================================
# 13. RUN APPLICATION
# ==========================================
root.mainloop()
