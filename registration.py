import customtkinter as ctk
import subprocess
import os
import sys
from client.company_info import get_company_info
from device.device_info import get_system_info
from client.register_employ import register_employee
from storage.register import save_registration_data, already_registered

def resource_path(filename):
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(__file__), filename)
def launch_launcher():
    if getattr(sys, "frozen", False):
        subprocess.Popen([resource_path("launcher.exe")])
    else:
        subprocess.Popen([sys.executable, resource_path("launcher.py")])

def run_extension_setup():
  
    if getattr(sys, "frozen", False):
        target = resource_path("extension_loader.exe")
        cmd = [target]
    else:
        target = resource_path("extension_loader.py")
        cmd = [sys.executable, target]

    print(f"Launching extension setup: {cmd}")

    if not os.path.exists(target):
        print(f"ERROR: extension setup target not found at: {target}")
        print("Skipping extension setup - check the path/build above.")
        return

    try:
        result = subprocess.run(cmd)
        print(f"Extension setup process exited with code {result.returncode}")
    except Exception as e:
        print(f"ERROR launching extension setup: {e}")


def safe_destroy(window):
    try:
        for after_id in window.tk.eval("after info").split():
            try:
                window.after_cancel(after_id)
            except Exception:
                pass
    except Exception:
        pass

    try:
        window.destroy()
    except Exception as e:
        print(f"Window teardown warning (ignored): {e}")
if already_registered():
    launch_launcher()
    sys.exit()


app = ctk.CTk()
app.title("ObserveX Agent Registration")
app.geometry("450x680")


title_label = ctk.CTkLabel(
    app,
    text="AGENT REGISTRATION",
    font=("Segoe UI", 20, "bold")
)
title_label.pack(pady=(25, 5))

subtitle_label = ctk.CTkLabel(
    app,
    text="Please fill in the details below to register.",
    font=("Segoe UI", 12),
    text_color="gray"
)
subtitle_label.pack(pady=(0, 15))


form_card = ctk.CTkFrame(app, corner_radius=12)
form_card.pack(padx=25, pady=(0, 20), fill="both", expand=True)


ctk.CTkLabel(form_card, text="Company Secret Token").pack(anchor="w", padx=25, pady=(20, 2))
token = ctk.CTkEntry(form_card, width=350)
token.pack(padx=25, pady=(0, 12))


ctk.CTkLabel(form_card, text="Name").pack(anchor="w", padx=25, pady=(0, 2))
name = ctk.CTkEntry(form_card, width=350)
name.pack(padx=25, pady=(0, 12))


ctk.CTkLabel(form_card, text="Email").pack(anchor="w", padx=25, pady=(0, 2))
email = ctk.CTkEntry(form_card, width=350)
email.pack(padx=25, pady=(0, 12))


ctk.CTkLabel(form_card, text="Phone").pack(anchor="w", padx=25, pady=(0, 2))
phone = ctk.CTkEntry(form_card, width=350)
phone.pack(padx=25, pady=(0, 12))


ctk.CTkLabel(form_card, text="Department").pack(anchor="w", padx=25, pady=(0, 2))
depart_box = ctk.CTkOptionMenu(form_card, values=[], width=350)
depart_box.pack(padx=25, pady=(0, 12))


ctk.CTkLabel(form_card, text="Designation").pack(anchor="w", padx=25, pady=(0, 2))
desig_box = ctk.CTkOptionMenu(form_card, values=[], width=350)
desig_box.pack(padx=25, pady=(0, 20))


departments = {}
designations = {}


def load_company_info():
    global departments, designations

    data = get_company_info(token.get())

    if data is None:
        print("Cannot connect to server.")
        return

    if data["status"] != "success":
        print(data["message"])
        return

    company = data["data"]

    departments = {
        d["name"]: d["id"]
        for d in company["departments"]
    }

    designations = {
        d["name"]: d["id"]
        for d in company["designations"]
    }

    depart_box.configure(values=list(departments.keys()))
    desig_box.configure(values=list(designations.keys()))

    if departments:
        depart_box.set(list(departments.keys())[0])

    if designations:
        desig_box.set(list(designations.keys())[0])

    print("Company info loaded successfully.")


def register_agent():

    device = get_system_info()

    payload = {
        "secret_token": token.get(),
        "name": name.get(),
        "email": email.get(),
        "phone": phone.get(),
        "department_id": departments.get(depart_box.get()),
        "designation_id": designations.get(desig_box.get()),

        "device_name": device["hostname"],
        "hostname": device["hostname"],
        "os": device["os"],
        "cpu": device["cpu"],
        "ram": device["ram"],
        "ip_address": device["ip_address"],
        "mac_address": device["mac_address"],
    }

    response = register_employee(payload)

    if response is None:
        print("Server not reachable.")
        return

    if response["status"] != "success":
        print(response["message"])
        return

    save_registration_data({
        "employee_id": response["employee_id"],
        "device_id": response["device_id"],
        "secret_token": token.get(),
        "name": name.get(),
        "email": email.get(),
        "phone": phone.get(),
        "department_id": departments.get(depart_box.get()),
        "designation_id": designations.get(desig_box.get()),
        "registered": True
    })
    print("Registration Successful")
    safe_destroy(app)
    run_extension_setup()
    launch_launcher()
load_button = ctk.CTkButton(
    app,
    text="Load Company Info",
    command=load_company_info
)
load_button.pack(pady=10)
register_button = ctk.CTkButton(
    app,
    text="Register Agent",
    command=register_agent
)
register_button.pack(pady=20)
app.mainloop()