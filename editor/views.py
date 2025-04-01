from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from arcgis.gis import GIS
from .models import Layer, Layergroup
import json
import os

# Create your views here.

# Login to AGO
gis = GIS("https://kantonbern.maps.arcgis.com/",
          "frei.hanskaspar_WEU_AWN", "Obiwan12#*")


def index(request):
    return render(request, 'editor/index.html')


def layers(request):
    queryset = Layer.objects.all()
    layerjson = serialize('json', queryset)
    return HttpResponse(layerjson, content_type='application/json')


def layergroups(request):
    queryset = Layergroup.objects.all().select_related()
    response = {"layergroups": []}
    for layergroup in queryset:
        response['layergroups'].append({
            "name": layergroup.name,
            "layers": []
        })
        layers = layergroup.layer.all()
        if (layers):
            for layer in layers:
                response['layergroups'][-1]['layers'].append({
                    "name": layer.name,
                    "description": layer.description
                })
    return HttpResponse(json.dumps(response), content_type='application/json')


def create_webmap(request):
    json_path = os.path.join(os.path.dirname(__file__), 'webMap2.json')
    with open(json_path) as json_data:
        webmap_dict = json.load(json_data)
    item_properties_dict = {
        "type": "Web Map",
        "title": "WebMap2 TEST",
        "tags": ["test", "test1", "test2"],
        "snippet": "This is a snippet",
        "overwrite": True,
        "text": webmap_dict
    }
    newmap = gis.content.add(item_properties=item_properties_dict)
    return render(request, 'editor/create_webmap_success.html')

# This view is for rendering the update webmap page


def edit_webmap(request):
    # get a list of existing webMaps
    webmaps = gis.content.search(
        query="type:Web Map AND owner:frei.hanskaspar_WEU_AWN", item_type="Web Map")
    return render(request, 'editor/update_webmap.html', {'webmaps': webmaps})


def update_webmap(request):
    if request.method == 'POST':
        # Get the selected webmap ID from the form submission
        selected_webmap_id = request.POST.get('webmap_select')

    # get the webmap item by its id
    item = gis.content.get(selected_webmap_id)

    updated_item_properties = {"title": "Updated WebMap2 TEST",
                               "snippet": "Dies ist eine WebMap welche aktualisiert wurde."
                               }

    # update the item properties
    item.update(item_properties=updated_item_properties)
    # Add the webmap item to the GIS content
    return JsonResponse({"success": True, "message": "Webmap updated successfully"})


def update_webmap_success(request):
    return render(request, 'editor/update_webmap_success.html')
