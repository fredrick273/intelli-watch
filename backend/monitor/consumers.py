from .models import System,SystemDataInstance
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer

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
            self.send("received")
        except:
            self.send("error")



# class execute(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.sysid = self.scope['url_route']['kwargs']['id']
#         await self.channel_layer.group_add(self.sysid, self.channel_name)
#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.sysid, self.channel_name)

#     async def receive(self, text_data=None, bytes_data=None):
#         print("Received data:", text_data)  
#         await self.channel_layer.group_send(
#             self.sysid,
#             {   
#                 "type": "command",
#                 "data": text_data,
#             },
#         )
