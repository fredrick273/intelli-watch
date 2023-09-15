from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse
from .models import System,SystemDataInstance
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

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
        try:
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
            }
            return render(request,"monitor/monitor.html",context=context)
        except:
            return HttpResponse("No data received yet")
    return HttpResponse("Unauthorized")

@login_required
def dashboard(request):
    systems = System.objects.filter(user = request.user)
    totalsys = len(systems)
    context = {
        "systems":systems,
        "total":totalsys
    }
    return render(request,"monitor/dashboard.html",context=context)

@login_required
def newsystem(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user = request.user
        system = System(name=name,user=user)
        system.save()
        base_file_path = os.path.join(settings.BASE_DIR,"client","client.py")
        with open(base_file_path, "r") as file:
            content = file.read()
        url = str(request.build_absolute_uri('/'))
        url = (url.split("/")[-2])
        url = 'ws://' + url + f"/ws/data/receive/{system.id}/"
        content = content.replace('ws://localhost:8000/ws/data/receive/1/', url)
        
        response = FileResponse(content)
        response['Content-Disposition'] = 'attachment; filename="client.py"'

        return response
    
@login_required
def multisystem(request):
    systems = System.objects.filter(user = request.user)
    context = {
        "systems":systems
    }
    return render(request,"monitor/multisystem.html",context=context)

@login_required
def showhistory(request,id):
    system = System.objects.get(id=id)
    user = request.user
    if user == system.user:
        systemdatas = SystemDataInstance.objects.filter(system=system)
        context = {
            'systemdatas':systemdatas,
            'id':id,
            'sys':system.name
        }
        return render(request,"monitor/history.html",context=context)

@login_required
def showhistorydata(request,id):
    systemdata = SystemDataInstance.objects.get(id=id)
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

    allsystemdata = SystemDataInstance.objects.filter(system = systemdata.system).order_by("-reported_time")
    index = list(allsystemdata).index(systemdata)
    previous_sysdata = allsystemdata[index:index+10]

    cpu_data = json.dumps([i.cpu_percent for i in previous_sysdata])
    memory_data = json.dumps([i.ram_percent for i in previous_sysdata])

            
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
    }
    return render(request,"monitor/monitor.html",context=context)