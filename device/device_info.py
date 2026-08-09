import socket
import psutil
import platform
import uuid
import cpuinfo
def get_address():
    mac = uuid.getnode()

    return ":".join(
        f"{(mac >> ele) & 0xFF:02X}"
        for ele in range(40, -1, -8)
    )
def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return "Unknown"
def get_system_info():
    system_info = {
        "os": platform.system(),
        "cpu": cpuinfo.get_cpu_info()['brand_raw'],
        "ram": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)}",
        "hostname": socket.gethostname(),
        "ip_address": get_ip_address(),
        "mac_address": get_address(),

    }
    return system_info

