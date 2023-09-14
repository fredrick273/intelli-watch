import os
import psutil
import windows_tools.antivirus
import windows_tools.windows_firewall
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import socket
import json
import subprocess
import requests
import json

def check_security():
    results = {}
    
    # Check antivirus status
    antivirus_enabled = is_antivirus_enabled()
    results["AntivirusEnabled"] = antivirus_enabled

    # Check Windows Firewall status
    firewall_enabled = is_firewall_enabled()
    results["FirewallEnabled"] = firewall_enabled

    # Check for removable USB devices
    usb_devices = get_usb_devices()
    results["USBDevices"] = usb_devices

    # Check network connections
    network_connections = get_network_stuff()
    results["NetworkConnections"] = network_connections

    # Check CPU and RAM usage
    cpu_percent = get_cpu_percent()
    results["CPUPercent"] = cpu_percent
    ram_percent = get_ram_percent()
    results["RAMPercent"] = ram_percent

    # Check recently modified files
    recent_files = get_recently_modified_files()
    results["RecentlyModifiedFiles"] = recent_files

    running_processes = get_running_processes()
    results["RunningProcesses"] = running_processes

    # Check installed software
    installed_software = get_installed_software()
    results["InstalledSoftware"] = installed_software

    # Check open ports
    # open_ports = get_open_ports()
    # results["OpenPorts"] = open_ports

    return results

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.modified_files = []  # Initialize an empty list to store modified file names

    def on_modified(self, event):
        if event.is_directory:
            return
        self.modified_files.append(event.src_path)  # Append the modified file name to the list

def get_recently_modified_files():
    print("Running modified files")
    handler = FileChangeHandler()
    path_to_watch = "C:\\Users\\Sam\\Desktop"
    file_observer = Observer()
    file_observer.schedule(handler, path=path_to_watch)
    file_observer.start()
    time.sleep(5)  # Wait for 60 seconds to collect modified files
    file_observer.stop()
    file_observer.join()
    print("Finished modified files")
    return handler.modified_files


# def get_open_ports():
#     print("Running open ports")
#     open_ports = []
#     for port in range(1, 1025):  # Check common ports
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(1)
#         result = sock.connect_ex(("localhost", port))
#         if result == 0:
#             open_ports.append(port)
#         sock.close()
#     print("Closed open ports")
#     return open_ports

def get_running_processes():
    print("Running open process")
    process_list = []
    for process in psutil.process_iter(attrs=["pid", "name"]):
        process_info = {
            "pid": process.info["pid"],
            "name": process.info["name"]
        }
        process_list.append(process_info)
    print("Closed open process")
    return process_list

def get_installed_software():
    print("Running installed process")
    installed_software = []
    try:
        result = subprocess.check_output(["wmic", "product", "get", "name"]).decode("utf-8")
        software_list = result.strip().split("\n")[1:]
        for software in software_list:
            installed_software.append(software.strip())
    except subprocess.CalledProcessError:
        pass
    print("Closed installed process")
    return installed_software

def is_antivirus_enabled():
    print("Running Antivius")
    result = windows_tools.antivirus.get_installed_antivirus_software()
    for i in result:
         if i["enabled"] == True:
              return True
    print("Closed Antivius")
    return False

def is_firewall_enabled():
    print("Closed Antivius")
    return windows_tools.windows_firewall.is_firewall_active()

def get_usb_devices():
    print("Running usb")
    current_usb_devices = []
    for device in psutil.disk_partitions():
        if "removable" in device.opts:
            current_usb_devices.append(device.device)
    print("Closed Usb")
    return current_usb_devices

def get_network_stuff():
    print("Running network")
    connections = psutil.net_connections(kind="inet")
    connection_list = []
    for conn in connections[:10]:
        local_address = f"{conn.laddr.ip}:{conn.laddr.port}"
        connection_info = {
            "local_address": local_address,
            "status": conn.status
        }
        if conn.raddr:
            remote_address = f"{conn.raddr.ip}:{conn.raddr.port}"
            connection_info["remote_address"] = remote_address
        connection_list.append(connection_info)
    print("Closed network")
    return connection_list

def get_cpu_percent():
    return psutil.cpu_percent(interval=5)

def get_ram_percent():
    return psutil.virtual_memory().percent

if __name__ == "__main__":
    security_results = check_security()
    print("Security Check Results:")
    # for key, value in security_results.items():
    #     print(f"{key}: {value}")
    # out_file = open("results.json", "w")
    # json.dump(security_results,out_file, indent = 6)
    # out_file.close()
    response = requests.post("http://127.0.0.1:8000/send/", 
    data=json.dumps(security_results),  # 
    headers={"Content-Type": "application/json"}, 
    )
    print(response.json())


