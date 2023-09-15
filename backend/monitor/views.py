from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import System,SystemDataInstance
from django.contrib.auth.decorators import login_required

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
    

@login_required
def viewreport(request,id):
    system = System.objects.get(id=id)
    user = request.user
    if user == system.user:
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
        report_time = systemdata.reported_time

        previous_sysdata = SystemDataInstance.objects.filter(system=system).order_by("-reported_time")[:10]
        cpu_data = json.dumps([i.cpu_percent for i in previous_sysdata])
        memory_data = json.dumps([i.ram_percent for i in previous_sysdata])
        prev_times = json.dumps([str(i.reported_time) for i in previous_sysdata])
        
        if (len(modified_files)==0):
            modified_files = 0

        if (len(usb)==0):
            usb = 0
        context = {
            "cpu_percent":cpu_percent,
            "ram_percent":ram_percent,
            "antivirus":antivirus,
            "firewall":firewall,
            "modified_files":modified_files,
            "running_processes":runningprocess[:10],
            "usb_devices":usb,
            "network_connections":network_connection,
            "installed_softwares":installed_softwares[:10],
            "report_time":report_time,
            "prev_cpu_data":cpu_data,
            "prev_ram_data":memory_data,
            "prev_times":prev_times
        }
        return render(request,"monitor/monitor.html",context=context)
    
    return HttpResponse("Unauthorized")

@login_required
def dashboard(request):

    pass

@login_required
def newsystem(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user = request.user
        system = System(name=name,user=user)
        system.save()

