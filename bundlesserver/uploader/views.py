import logging
import json
from os import path, makedirs
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def upload(request):
    try:
        return unsafe_upload(request)
    except Exception as e:
        logging.exception("Bad thing happen:")
        return HttpResponseServerError("Server Error: %s" %  e)


@csrf_exempt
def upload5(request):
    try:
        return unsafe_upload5(request)
    except Exception as e:
        logging.exception("Bad think happen:")
        return HttpResponseServerError("Server Error: %s" % e)        

def unsafe_upload(request):
    #print "Strt uploading, method:", request.method
    #print request.body
    #print request.POST["name"], "=", request.POST["version"]
    #print request.FILES["data"]
    app_version = request.POST["app_version"]
    home = path.join(settings.DATA_PATH, app_version)
    if not path.exists(home):
        makedirs(home)
    versions = {}
    versions_file = path.join(home, "versions.json")
    if path.exists(versions_file):
        with open(versions_file, "r") as f:
            versions = json.load(f)

    versions[request.POST["name"]] = request.POST["version"]
    with open(versions_file, "w") as f:
        json.dump(versions, f)

    targetfilename = path.join(home, request.POST["name"])
    if not path.exists(path.dirname(targetfilename)):
        makedirs(path.dirname(targetfilename))
    with open(targetfilename, "w") as targetfile:
        for chunk in request.FILES["data"].chunks():
            targetfile.write(chunk)
    return HttpResponse("OK")


def unsafe_upload5(request):
    app_version = request.POST["app_version"]
    home = path.join(settings.DATA_PATH, app_version)
    if not path.exists(home):
        makedirs(home)

    targetfilename = path.join(home, request.POST["name"])
    if not path.exists(path.dirname(targetfilename)):
        makedirs(path.dirname(targetfilename))

    with open(targetfilename, "w") as targetfile:
        for chunk in request.FILES["data"].chunks():
            targetfile.write(chunk)

    return HttpResponse("OK")



