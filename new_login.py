import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from escpos.printer import Usb

# === USB Printer Settings ===
VENDOR_ID = 0x0485
PRODUCT_ID = 0x5741
printer = Usb(VENDOR_ID, PRODUCT_ID)

printer.set(align='center', font='b', width=1, height=1)

# === Approved Names ===
people = ["Andrew Dimery", "Big Carl", "Micheal", "Alex"]
person_count = 1
group_count = 1

# === Main Window Setup ===
root = tk.Tk()
root.title("CLUES Canasta Familiar")
root.geometry("900x600")
root.configure(bg="#000000")

content_frame = tk.Frame(root, bg="#000000")
content_frame.pack(fill='both', expand=True)

# === Utility ===
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def printer_print(name, person, group):
    printer.text(f"Welcome : {name} \n\n")
    printer.text(f"You are part of group {group} \n")
    printer.text(f"Number {person}")
    printer.cut()

# === UI Screens ===
def show_scan_screen():
    clear_content()
    scan_screen = tk.Frame(content_frame, bg="#f89f4f")
    scan_screen.pack(fill='both', expand=True)

    title = tk.Label(scan_screen, text="Welcome to CLUES Canasta Familiar",
                     font=("Georgia", 28, "bold"), fg="white", bg="#f89f4f", pady=10)
    title.pack()

    subtitle = tk.Label(scan_screen,
                        text="Our self-service ticketing system helps you access fresh produce, meat, and cultural foods quickly and efficiently.",
                        font=("Georgia", 12), fg="white", bg="#f89f4f", wraplength=800, justify="center")
    subtitle.pack()

    note = tk.Label(scan_screen,
                    text="If you do not have a card, please see our friendly staff for assistance in obtaining one.",
                    font=("Georgia", 12), fg="white", bg="#f89f4f", pady=10)
    note.pack()

    scan_text = tk.Label(scan_screen, text="Please scan your card / Por favor escanea tu tarjeta",
                         font=("Georgia", 22, "bold"), fg="#3c2f1c", bg="#f89f4f", pady=20)
    scan_text.pack()

    try:
        image = Image.open("scan_card.png")
        image = image.resize((200, 200), Image.LANCZOS)
        scan_img = ImageTk.PhotoImage(image)
        img_label = tk.Label(scan_screen, image=scan_img, bg="#f89f4f")
        img_label.image = scan_img
        img_label.pack(pady=10)
    except:
        error_label = tk.Label(scan_screen, text="(Image failed to load)", fg="red", bg="#f89f4f")
        error_label.pack()

    global status_label
    status_label = tk.Label(scan_screen, text="Waiting for RFID...", font=("Georgia", 14), fg="white", bg="#f89f4f")
    status_label.pack(pady=20)

def show_validated_screen(name, person, group):
    clear_content()
    validated_screen = tk.Frame(content_frame, bg="#000000")
    validated_screen.pack(fill='both', expand=True)

    header = tk.Label(validated_screen, text="Validation Successful!",
                      font=("Georgia", 28, "bold"), fg="white", bg="#000000", pady=20)
    header.pack()

    subtext = tk.Label(validated_screen,
                       text=f"{name}, you’ve been validated.\nPlease collect your receipt.",
                       font=("Georgia", 14), fg="white", bg="#000000")
    subtext.pack(pady=10)

    try:
        check_img = Image.open("validated_check.png")
        check_img = check_img.resize((120, 120), Image.LANCZOS)
        check_photo = ImageTk.PhotoImage(check_img)
        img_label = tk.Label(validated_screen, image=check_photo, bg="#000000")
        img_label.image = check_photo
        img_label.pack(pady=10)
    except:
        fallback = tk.Label(validated_screen, text="✓", font=("Georgia", 50), fg="#f89f4f", bg="#000000")
        fallback.pack(pady=10)

    root.after(10000, show_scan_screen)

def show_denied_screen(message):
    clear_content()
    denied_screen = tk.Frame(content_frame, bg="#330000")
    denied_screen.pack(fill='both', expand=True)

    header = tk.Label(denied_screen, text="Card Not Recognized",
                      font=("Georgia", 28, "bold"), fg="white", bg="#330000", pady=20)
    header.pack()

    detail = tk.Label(denied_screen,
                      text=message + "\nPlease scan again.",
                      font=("Georgia", 14), fg="white", bg="#330000")
    detail.pack(pady=10)

    try:
        warning_img = Image.open("denied_icon.png")
        warning_img = warning_img.resize((120, 120), Image.LANCZOS)
        warning_photo = ImageTk.PhotoImage(warning_img)
        img_label = tk.Label(denied_screen, image=warning_photo, bg="#330000")
        img_label.image = warning_photo
        img_label.pack(pady=10)
    except:
        fallback = tk.Label(denied_screen, text="✗", font=("Georgia", 50), fg="red", bg="#330000")
        fallback.pack(pady=10)

    root.after(5000, show_scan_screen)

# === RFID Scanning Logic ===
def scan_loop():
    global person_count, group_count
    reader = SimpleMFRC522()

    while True:
        try:
            set_status("Waiting for RFID...", "white")
            id, text = reader.read()
            cleaned_text = text.strip()
            print("Scanned:", cleaned_text)

            if cleaned_text == "":
                set_status("Scan Error: Empty tag", "orange")
                show_denied_screen("Card read failed or is blank.")
            elif cleaned_text in people:
                set_status(f"Welcome, {cleaned_text}", "green")
                printer_print(cleaned_text, person_count, group_count)
                show_validated_screen(cleaned_text, person_count, group_count)

                person_count += 1
                if person_count == 5:
                    person_count = 1
                    group_count += 1
            else:
                set_status(f"Access Denied: '{cleaned_text}'", "red")
                show_denied_screen(f"'{cleaned_text}' is not authorized.")

        except Exception as e:
            print("RFID Error:", e)
            set_status(f"Error: {str(e)}", "red")
            show_denied_screen("There was an error reading your card.")

        time.sleep(5)

def set_status(message, color):
    if 'status_label' in globals():
        status_label.config(text=message, fg=color)

# === Cleanup on Close ===
def on_closing():
    GPIO.cleanup()
    root.destroy()

# === Start App ===
show_scan_screen()
threading.Thread(target=scan_loop, daemon=True).start()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
