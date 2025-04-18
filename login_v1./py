import tkinter as tk
from tkinter import messagebox
import threading
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# List of allowed names (must match RFID tag text exactly)
people = ["Andrew Dimery", "Big Car;"]

def read_rfid():
    reader = SimpleMFRC522()
    print("Hold a tag near the reader...")
    id, text = reader.read()
    cleaned_text = text.strip()
    print("Tag UID:", id)
    print("Tag text:", cleaned_text)
    print("Raw tag text:", repr(text))
    return cleaned_text

class RFIDLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID Login")

        self.label = tk.Label(root, text="Please scan your RFID card", font=("Arial", 14))
        self.label.pack(pady=20)

        self.status = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.status.pack(pady=10)

        self.login_button = tk.Button(root, text="Scan RFID", command=self.start_scan_thread)
        self.login_button.pack(pady=20)

    def start_scan_thread(self):
        # Disable the button during the scan
        self.login_button.config(state=tk.DISABLED)
        self.status.config(text="Waiting for RFID...")
        threading.Thread(target=self.scan_rfid, daemon=True).start()

    def scan_rfid(self):
        print("[Thread] Starting RFID read...")
        try:
            tag_text = read_rfid()
            print("[Thread] Read complete.")
            self.root.after(0, self.check_login, tag_text)
        except Exception as e:
            print("[Thread] Error during RFID read:", e)
            self.root.after(0, lambda: messagebox.showerror("RFID Error", str(e)))

    def check_login(self, tag_text):
        if tag_text in people:
            self.status.config(text=f"Welcome, {tag_text}!", fg="green")
        else:
            self.status.config(text="Access Denied", fg="red")
            messagebox.showerror("Error", f"'{tag_text}' is not authorized.")

        # Reset status to blue after 3 seconds
        self.root.after(3000, lambda: self.reset_button())

    def reset_button(self):
        # Reset the status and re-enable the button
        self.status.config(text="Waiting for RFID...", fg="blue")
        self.login_button.config(state=tk.NORMAL)  # Enable the button again

def on_closing():
    print("Cleaning up GPIO...")
    GPIO.cleanup()
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDLoginApp(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
