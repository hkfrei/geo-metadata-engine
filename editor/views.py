from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from arcgis.gis import GIS
from .models import Layer, Layergroup, Webmap
import json
import os

# Create your views here.

# Login to AGO
gis = GIS('https://kantonbern.maps.arcgis.com/',
          'frei.hanskaspar_WEU_AWN', 'Obiwan12#*')


def index(request):
    return render(request, 'editor/index.html')


def layers(request):
    queryset = Layer.objects.all()
    layerjson = serialize('json', queryset)
    return HttpResponse(layerjson, content_type='application/json')


def layergroups(request):
    queryset = Layergroup.objects.all().select_related()
    response = {'layergroups': []}
    for layergroup in queryset:
        response['layergroups'].append({
            'name': layergroup.name,
            'layers': []
        })
        layers = layergroup.layer.all()
        if (layers):
            for layer in layers:
                response['layergroups'][-1]['layers'].append({
                    'name': layer.name,
                    'description': layer.description
                })
    return HttpResponse(json.dumps(response), content_type='application/json')


def create_webmap(request):
    webmapconfigs = Webmap.objects.all()
    return render(request, 'editor/create_webmap.html', {'webmapconfigs': webmapconfigs})


def save_webmap(request):
    if request.method == 'POST':
        webmapname = request.POST['webmap_config_select']
        webmap = Webmap.objects.filter(title=webmapname)
        title = webmap[0].title
        description = webmap[0].description
        snippet = webmap[0].snippet
        culture = webmap[0].culture

        json_path = os.path.join(os.path.dirname(__file__), 'webMap2.json')
        with open(json_path) as json_data:
            webmap_dict = json.load(json_data)

        item_properties_dict = {
            'type': 'Web Map',
            'title': title,
            'description': description,
            'tags': ['test', 'test1', 'test2'],
            'snippet': snippet,
            'overwrite': True,
            'text': webmap_dict
        }
        gis.content.add(item_properties=item_properties_dict)
    return JsonResponse({'success': True, 'message': 'Webmap created successfully'})


# This view is for rendering the update webmap page


def edit_webmap(request):
    # get a list of existing webMaps
    webmaps = gis.content.search(
        query='type:Web Map AND owner:frei.hanskaspar_WEU_AWN', item_type='Web Map')
    return render(request, 'editor/update_webmap.html', {'webmaps': webmaps})


def update_webmap(request):
    if request.method == 'POST':
        # Get the selected webmap ID from the form submission
        selected_webmap_id = request.POST.get('webmap_select')

    # get the webmap item by its id
    item = gis.content.get(selected_webmap_id)

    updated_item_properties = {'title': 'Updated WebMap2 TEST',
                               'snippet': 'Dies ist eine WebMap welche aktualisiert wurde.'
                               }

    # update the item properties
    item.update(item_properties=updated_item_properties)
    # Add the webmap item to the GIS content
    return JsonResponse({'success': True, 'message': 'Webmap updated successfully'})


def update_webmap_success(request):
    return render(request, 'editor/update_webmap_success.html')


def create_webmap_success(request):
    return render(request, 'editor/create_webmap_success.html')
