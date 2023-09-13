from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Temp
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