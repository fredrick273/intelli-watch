import threading
import psutil
import windows_tools.antivirus
import windows_tools.windows_firewall
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
import subprocess
import json
import os
import winreg as reg
import asyncio
import websockets


report_interval = 20

def check_security():
    results = {}
    threads = [] 

    def collect_antivirus_status():
        antivirus_enabled = is_antivirus_enabled()
        results["AntivirusEnabled"] = antivirus_enabled

    def collect_firewall_status():
        firewall_enabled = is_firewall_enabled()
        results["FirewallEnabled"] = firewall_enabled

    def collect_usb_devices():
        usb_devices = get_usb_devices()
        results["USBDevices"] = usb_devices

    def collect_network_connections():
        network_connections = get_network_stuff()
        results["NetworkConnections"] = network_connections

    def collect_cpu_and_ram_usage():
        cpu_percent = get_cpu_percent()
        results["CPUPercent"] = cpu_percent
        ram_percent = get_ram_percent()
        results["RAMPercent"] = ram_percent

    def collect_recently_modified_files():
        recent_files = get_recently_modified_files()
        results["RecentlyModifiedFiles"] = recent_files

    def collect_running_processes():
        running_processes = get_running_processes()
        results["RunningProcesses"] = running_processes

    def collect_installed_software():
        installed_software = get_installed_software()
        results["InstalledSoftware"] = installed_software

    # Create threads for each data collection function
    threads.append(threading.Thread(target=collect_firewall_status))
    threads.append(threading.Thread(target=collect_usb_devices))
    threads.append(threading.Thread(target=collect_network_connections))
    threads.append(threading.Thread(target=collect_cpu_and_ram_usage))
    threads.append(threading.Thread(target=collect_recently_modified_files))
    threads.append(threading.Thread(target=collect_running_processes))
    threads.append(threading.Thread(target=collect_installed_software))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    collect_antivirus_status()
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
    time.sleep(report_interval)  # Wait for 60 seconds to collect modified files
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
    installed_software_with_date = []
    try:
        result = subprocess.check_output(["wmic", "product", "get", "name,installdate"]).decode("utf-8")
        lines = result.strip().split("\n")
        header = [s.strip() for s in lines[0].split()]
        for line in lines[1:]:
            values = [s.strip() for s in line.split(None, len(header) - 1)]
            if len(values) == len(header):
                software_info = dict(zip(header, values))
                installed_software_with_date.append(software_info)
    except subprocess.CalledProcessError:
        pass
    print("Closed installed process")
    return installed_software_with_date
    

def is_antivirus_enabled():
    print("Running Antivius")
    result = windows_tools.antivirus.get_installed_antivirus_software()
    for i in result:
         if i["enabled"] == True:
              print("Antivirus True")
              return True
    print("Closed Antivius")
    print("Antivirus False")
    return False

def is_firewall_enabled():
    print("Closed Antivius")
    return windows_tools.windows_firewall.is_firewall_active()

def get_usb_devices():
    print("Running usb")
    current_usb_devices = []
    t_end = time.time() + report_interval
    while time.time() < t_end:
        for device in psutil.disk_partitions():
            if "removable" in device.opts:
                if not device.device in current_usb_devices:
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
        else:
            connection_info["remote_address"] = ""
        connection_list.append(connection_info)
    print("Closed network")
    return connection_list

def get_cpu_percent():
    return psutil.cpu_percent(interval=5)

def get_ram_percent():
    return psutil.virtual_memory().percent

def AddToRegistry():
    pth = os.path.dirname(os.path.realpath(__file__))
    s_name = "client.py"
    address = os.path.join(pth, s_name)

    key = reg.HKEY_CURRENT_USER
    key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        # Open the registry key
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_READ)

        # Try to retrieve the existing value
        existing_value, _ = reg.QueryValueEx(open_key, "monitor")

        if existing_value != address:
            # If the value is different, update it
            reg.SetValueEx(open_key, "monitor", 0, reg.REG_SZ, address)

        reg.CloseKey(open_key)

    except FileNotFoundError:
        # If the key doesn't exist, create it
        reg.CreateKey(key, key_value)
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_WRITE)
        reg.SetValueEx(open_key, "monitor", 0, reg.REG_SZ, address)
        reg.CloseKey(open_key)



def main():

    while True:


        security_results = check_security()
        print("Security Check Results:")

        async def test():
            async with websockets.connect('ws://localhost:8000/ws/data/receive/1/') as websocket:
                await websocket.send(json.dumps(security_results))
                response = await websocket.recv()
                print(response)

        asyncio.get_event_loop().run_until_complete(test())

        

if __name__ == "__main__":
    AddToRegistry()
    main()

