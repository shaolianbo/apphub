import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from app_spider.management.commands.run_spider import Command


@csrf_exempt
@require_POST
def crawl(request):
    apk_names = request.POST.getlist('apk_names', [])
    top_type = request.POST.get('top_type', 0)
    if not (apk_names and top_type):
        return HttpResponseBadRequest('post param wrong')
    c = Command(apk_names, top_type)
    saved_apps = c.crawl()
    resp_body = dict(
        success=len(saved_apps) == len(apk_names),
        saved_apps=saved_apps
    )
    resp = HttpResponse(json.dumps(resp_body))
    return resp
