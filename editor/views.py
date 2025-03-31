from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from arcgis.gis import GIS
from arcgis.mapping import WebMap
from .models import Layer, Layergroup
import json
import os

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

def create_webmap(request):
    gis=GIS("https://kantonbern.maps.arcgis.com/","frei.hanskaspar_WEU_AWN","Obiwan12#*")
    print("Successfully logged in as: " + gis.properties.user.username)
    json_path = os.path.join(os.path.dirname(__file__), 'webMap.json')
    with open(json_path) as json_data:
        webmap_dict = json.load(json_data)
    item_properties_dict = {
        "type": "Web Map",
        "title": "Test Map",
        "tags": ["test","test1","test2"],
        "snippet":"This is a snippet", 
        "overwrite":True,
        "text":webmap_dict
        }
    newmap = gis.content.add(item_properties=item_properties_dict)
    print("newmap successfully created", newmap)
    return render(request, 'editor/webmap.html')
       
        
    
    