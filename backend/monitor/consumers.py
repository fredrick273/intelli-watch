from .models import System,SystemDataInstance,Notifier
from channels.generic.websocket import WebsocketConsumer
import requests
webhook_url = "https://discord.com/api/webhooks/1152515332947329054/vDk9wmtPWSHfTJM93cLAKq8mS5r8lt4AkYDfmGOJpT_2vtK7CNjiEqUViaRT8uOkvD7l"


import json

class data(WebsocketConsumer):
    def connect(self):
        self.sysid = self.scope['url_route']['kwargs']['id']
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None):
        try:
            system = System.objects.get(id=self.sysid)
            data = json.loads(text_data)
            cpu_percent = data["CPUPercent"]
            ram_percent = data["RAMPercent"]
            modifiedfiles = json.dumps({"files":data["RecentlyModifiedFiles"]})
            runningprocess = json.dumps({"process":data["RunningProcesses"]})
            usb = json.dumps({"usb":data["USBDevices"]})
            antivirus = data["AntivirusEnabled"]
            firewall = data["FirewallEnabled"]
            network_connection = json.dumps({"network":data["NetworkConnections"]})
            installed_software = json.dumps({"installed":data["InstalledSoftware"]})

            systemdata = SystemDataInstance(system=system,anti_virus_status=antivirus,firewall_virus_status=firewall,cpu_percent=cpu_percent,ram_percent=ram_percent,running_process=runningprocess,usb_devices=usb,modified_files=modifiedfiles,network_connection=network_connection,installed_softwares=installed_software)
            systemdata.save()
            user = systemdata.system.user
            if Notifier.objects.filter(user = user).exists():
                notifier = Notifier.objects.get(user = user)
            else:
                notifier = False

            if (not antivirus) and system.antivirus_notification and notifier:
                content = f"Anti virus has been turned of for {system.name}"
                message = {"content": content}
                requests.post(notifier.webhook, json=message)

            if (not firewall) and system.firewall_notification and notifier:
                content = f"Firewall has been turned off for {system.name}"
                message = {"content": content}
                requests.post(notifier.webhook, json=message)
           
            self.send("received")
        except:
            self.send("error")

