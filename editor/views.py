from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import Layer, Layergroup
import json

# Create your views here.
def index(request):
    return render(request, 'editor/index.html')

def layers(request):
    queryset = Layer.objects.all()
    layerjson = serialize('json', queryset)
    return HttpResponse(layerjson, content_type='application/json')

def layergroups(request):
    queryset = Layergroup.objects.all().select_related()
    response = {"layergroups":[]}
    for layergroup in queryset:
        response['layergroups'].append({
            "name":layergroup.name, 
            "layers":[]
            })
        layers = layergroup.layer.all()
        if(layers):
            for layer in layers:
                response['layergroups'][-1]['layers'].append({
                    "name":layer.name,
                    "description":layer.description
                    })
    return HttpResponse(json.dumps(response), content_type='application/json')
       
        
    
    