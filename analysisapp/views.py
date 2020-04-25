import json
from django.http import HttpResponse
from analysisapp.services import analyze

def show_analysis(request):
    return HttpResponse(analyze(request.GET.get("text")))