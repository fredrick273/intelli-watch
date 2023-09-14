from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Temp,System,SystemDataInstance
# Create your views here.

@csrf_exempt
def receive(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            savepoint = Temp.objects.get(id=1)
            savepoint.data = json.dumps(data)
            savepoint.save()
            return JsonResponse({'message':'sucess'})
        except:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
    else:
        return HttpResponse("Hello world")
    
def seedata(request):
    text = f"{Temp.objects.get(id=1).data}"
    data = json.loads(text)
    return JsonResponse(data)


@csrf_exempt
def report(request,id):
    if request.method == "POST":
        system = System.objects.get(id=id)
        try:
            data = json.loads(request.body)
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

            return JsonResponse({'message':'sucess'})
        except:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
    else:
        system = System.objects.get(id=id)
        return HttpResponse(system.name)

def viewreport(request,id):
    system = System.objects.get(id=id)
    systemdata = SystemDataInstance.objects.filter(system=system).last()
    cpu_percent = systemdata.cpu_percent
    ram_percent = systemdata.ram_percent
    antivirus = systemdata.anti_virus_status
    firewall = systemdata.firewall_virus_status
    modified_files = json.loads(systemdata.modified_files)["files"]
    runningprocess = json.loads(systemdata.running_process)["process"]
    usb = json.loads(systemdata.usb_devices)["usb"]
    network_connection = json.loads(systemdata.network_connection)["network"]
    installed_softwares = json.loads(systemdata.installed_softwares)["installed"]
    print(installed_softwares)

    context = {
        "cpu_percent":cpu_percent,
        "ram_percent":ram_percent,
        "antivirus":antivirus,
        "firewall":firewall,
        "modified_files":modified_files,
        "running_processes":runningprocess[:10],
        "usb_devices":usb,
        "network_connections":network_connection,
        "installed_softwares":installed_softwares
    }
    return render(request,"monitor/report.html",context=context)

