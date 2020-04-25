import json
from django.http import HttpResponse
from analysisapp.services import analyze

def show_analysis(request):
    response_data = analyze(request.GET.get("text"))
    return HttpResponse(json.dumps(response_data, ensure_ascii=False),
         content_type="application/json")