from django.db import models
from users.models import UserData


class System(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(UserData,on_delete=models.CASCADE)
    antivirus_notification = models.BooleanField(default=False)
    firewall_notification = models.BooleanField(default=False)

class SystemDataInstance(models.Model):
    system = models.ForeignKey(System,on_delete=models.CASCADE)
    reported_time = models.DateTimeField(auto_now_add=True)
    anti_virus_status = models.BooleanField(default=False)
    firewall_virus_status = models.BooleanField(default=False)
    cpu_percent = models.FloatField()
    ram_percent = models.FloatField()
    running_process = models.TextField()
    usb_devices = models.TextField()
    modified_files = models.TextField()
    network_connection = models.TextField()
    installed_softwares = models.TextField(null=True)