import windows_tools.antivirus
import windows_tools.windows_firewall
import psutil
import requests
import threading
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def is_antivirus_enabled():
    antivirus_result = windows_tools.antivirus.get_installed_antivirus_software()
    return bool(antivirus_result)
# Initialize the status of antivirus and firewall
antivirus_disabled =not is_antivirus_enabled()
firewall_disabled = not windows_tools.windows_firewall.is_firewall_active()

webhook_url = 'DISCORD_WEBHOOK_LINK_HERE'
cpu_threshold = 90
network_threshold = 1024 * 1024 * 10

connected_usb_devices = []

connected_usb_devices = []

def monitor_usb_devices():
    while True:
        # Get a list of currently connected USB devices
        current_usb_devices = []
        for device in psutil.disk_partitions():
            if 'removable' in device.opts:
                current_usb_devices.append(device.device)

        # Check for newly connected USB devices
        new_devices = set(current_usb_devices) - set(connected_usb_devices)
        if new_devices:
            for device in new_devices:
                message = f"USB device connected: {device}"
                send_discord_alert(message)

        # Check for disconnected USB devices
        disconnected_devices = set(connected_usb_devices) - set(current_usb_devices)
        if disconnected_devices:
            for device in disconnected_devices:
                message = f"USB device disconnected: {device}"
                send_discord_alert(message)

        # Update the list of connected USB devices
        connected_usb_devices[:] = current_usb_devices

        time.sleep(60)  

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        message = f"File modified: {event.src_path}"
        send_discord_alert(message)

def send_discord_alert(message):
    payload = {'content': message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Alert sent successfully to Discord!")
    else:
        print("Failed to send alert to Discord. Status code:", response.status_code)

def monitor_network():
    while True:
        network_info = psutil.net_io_counters()
        sent_speed = network_info.bytes_sent
        recv_speed = network_info.bytes_recv

        if sent_speed > network_threshold or recv_speed > network_threshold:
            message = f"Abnormal network traffic detected: Sent={sent_speed} B, Recv={recv_speed} B"
            send_discord_alert(message)

        time.sleep(5)

def monitor_and_send_security_events():
    global antivirus_disabled, firewall_disabled
    while True:
        # Check for security events in Security Event Log
        cmd = 'powershell Get-WinEvent -LogName Security | Where-Object {$_.Id -eq 4625}'
        event_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = event_output.communicate()

        if "EventId : 4625" in output.decode('utf-8'):
            message = "Authentication failure detected"
            send_discord_alert(message)

        # Check if antivirus is disabled
        if not antivirus_disabled:
            antivirus_result = is_antivirus_enabled()
            print(antivirus_result)
            if not (antivirus_result):
                message = "Antivirus is turned off!"
                send_discord_alert(message)
                antivirus_disabled = True
            else:
                message = "Antivirus is turned back on!"
                send_discord_alert(message)
                antivirus_disabled = False

        if not firewall_disabled:
            firewall_status = windows_tools.windows_firewall.is_firewall_active()
            if not firewall_status:
                message = "Firewall is turned off!"
                send_discord_alert(message)
                firewall_disabled = True
            else:
                message = "Firewall is turned back on!"
                send_discord_alert(message)
                firewall_disabled = False

        time.sleep(60)


def monitor_cpu_usage():
    while True:
        cpu_percent = psutil.cpu_percent(interval=5)
        if cpu_percent > cpu_threshold:
            message = f"High CPU usage detected: {cpu_percent}%"
            send_discord_alert(message)
        time.sleep(60)

if __name__ == "__main__":
    print("Monitoring for security events...")

    network_thread = threading.Thread(target=monitor_network)
    network_thread.start()

    auth_failure_thread = threading.Thread(target=monitor_and_send_security_events)
    auth_failure_thread.start()

    cpu_usage_thread = threading.Thread(target=monitor_cpu_usage)
    cpu_usage_thread.start()

    file_observer = Observer()
    # Replace 'C:\\path\\to\\monitor' with the directory path you want to observe on Windows.
    file_observer.schedule(FileChangeHandler(), path='PATH')
    file_observer.start()

    usb_device_thread = threading.Thread(target=monitor_usb_devices)
    usb_device_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    network_thread.join()
    auth_failure_thread.join()
    cpu_usage_thread.join()
    file_observer.stop()
    file_observer.join()
    usb_device_thread.join()
