import customtkinter as ctk
import subprocess
import os
import sys


def resource_path(path):
    if getattr(sys, "frozen", False):
        return os.path.join(
            os.path.dirname(sys.executable),
            path
        )
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        path
    )

def open_chrome():
    folder = resource_path("extensions/chrome")
    subprocess.Popen(["explorer.exe", folder])
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome):
        subprocess.Popen([chrome, "--new-window", "chrome://extensions/"])

def open_edge():
    folder = resource_path("extensions/edge")
    subprocess.Popen(["explorer.exe", folder])
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge):
        subprocess.Popen([edge, "--new-window", "edge://extensions/"])

def install_extension():
    app = ctk.CTk()
    app.title("ObserveX Extension Setup")
    app.geometry("760x540")
    app.resizable(False, False)

    chrome_done_var = ctk.IntVar(value=0)
    edge_done_var = ctk.IntVar(value=0)

    def check_progress():
        if chrome_done_var.get() == 1 and edge_done_var.get() == 1:
            finish_button.configure(state="normal", fg_color="#1f538d", hover_color="#14375e")
        else:
            finish_button.configure(state="disabled", fg_color="gray")

    def finish_setup():
        app.destroy()  

    title = ctk.CTkLabel(
        app,
        text="ObserveX Browser Extension Setup",
        font=("Segoe UI", 24, "bold")
    )
    title.pack(pady=(20, 5))

    subtitle = ctk.CTkLabel(
        app,
        text="This is a ONE TIME setup. Complete both steps to start the agent.",
        font=("Segoe UI", 12, "italic"),
        text_color="gray"
    )
    subtitle.pack(pady=(0, 15))

    columns_frame = ctk.CTkFrame(app, fg_color="transparent")
    columns_frame.pack(fill="both", expand=True, padx=20, pady=5)

    chrome_card = ctk.CTkFrame(columns_frame, corner_radius=10)
    chrome_card.pack(side="left", fill="both", expand=True, padx=10, pady=5)

    chrome_header = ctk.CTkLabel(
        chrome_card,
        text="GOOGLE CHROME",
        font=("Segoe UI", 14, "bold"),
        text_color="#4285F4"
    )
    chrome_header.pack(pady=(15, 5))
    chrome_badge = ctk.CTkLabel(
        chrome_card,
        text="Chrome Setup Steps",
        height=32,
        fg_color="#4285F4",
        text_color="white",
        corner_radius=6,
        font=("Segoe UI", 12, "bold")
    )
    chrome_badge.pack(pady=10, padx=15, fill="x")

    chrome_steps_text = (
        "1. Open Google Chrome.\n\n"
        "2. Go to: chrome://extensions/\n\n"
        "3. Open the extension folder.\n\n"
        "4. Turn on Developer Mode (top-right).\n\n"
        "5. Click Load unpacked and select chrome."
    )
    
    chrome_steps = ctk.CTkLabel(
        chrome_card,
        text=chrome_steps_text,
        justify="left",
        font=("Segoe UI", 11)
    )
    chrome_steps.pack(padx=15, pady=(5, 15), anchor="w")

    chrome_checkbox = ctk.CTkCheckBox(
        chrome_card,
        text="I have set up Chrome",
        variable=chrome_done_var,
        command=check_progress,
        font=("Segoe UI", 11, "bold"),
        fg_color="#4285F4",
        hover_color="#357ae8"
    )
    chrome_checkbox.pack(pady=(0, 15))

    edge_card = ctk.CTkFrame(columns_frame, corner_radius=10)
    edge_card.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    edge_header = ctk.CTkLabel(
        edge_card,
        text="MICROSOFT EDGE",
        font=("Segoe UI", 14, "bold"),
        text_color="#107C41"
    )
    edge_header.pack(pady=(15, 5))
    edge_badge = ctk.CTkLabel(
        edge_card,
        text="Edge Setup Steps",
        height=32,
        fg_color="#107C41",
        text_color="white",
        corner_radius=6,
        font=("Segoe UI", 12, "bold")
    )
    edge_badge.pack(pady=10, padx=15, fill="x")

    edge_steps_text = (
        "1. Open Microsoft Edge.\n\n"
        "2. Go to: edge://extensions/\n\n"
        "3. Open the extension folder.\n\n"
        "4. Turn on Developer Mode (bottom-left).\n\n"
        "5. Click Load unpacked and select edge."
    )

    edge_steps = ctk.CTkLabel(
        edge_card,
        text=edge_steps_text,
        justify="left",
        font=("Segoe UI", 11)
    )
    edge_steps.pack(padx=15, pady=(5, 15), anchor="w")

    edge_checkbox = ctk.CTkCheckBox(
        edge_card,
        text="I have set up Edge",
        variable=edge_done_var,
        command=check_progress,
        font=("Segoe UI", 11, "bold"),
        fg_color="#107C41",
        hover_color="#0b5e31"
    )
    edge_checkbox.pack(pady=(0, 15))


    footer_frame = ctk.CTkFrame(app, fg_color="transparent")
    footer_frame.pack(fill="x", padx=30, pady=(15, 20))

    finish_button = ctk.CTkButton(
        footer_frame,
        text="Finish Setup & Launch ObserveX",
        height=40,
        state="disabled", 
        fg_color="gray",
        font=("Segoe UI", 13, "bold"),
        command=finish_setup
    )
    finish_button.pack(fill="x")

    app.mainloop()
if __name__ == "__main__":
    install_extension()