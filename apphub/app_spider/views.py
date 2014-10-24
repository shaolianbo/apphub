from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET

from app_spider.management.commands.run_spider import Command
from store.models import AppInfo


@require_GET
def crawl(request):
    apk_names = request.GET.getlist('apk_names', [])
    top_type = request.GET.get('top_type', 0)
    if not (apk_names and top_type):
        return HttpResponseBadRequest('post param wrong')
    c = Command(apk_names, top_type)
    saved_apps = c.crawl()
    resp_body = dict(
        success=len(saved_apps) == len(apk_names),
        saved_apps=saved_apps
    )
    return JsonResponse(resp_body)


@require_GET
def change_continue(request):
    apk_names = request.GET.getlist('apk_names', [])
    error = {}
    success = True
    for apk_name in apk_names:
        try:
            appinfo = AppInfo.objects.get(app_id__apk_name=apk_name)
        except AppInfo.DoesNotExist:
            error[apk_name] = 'not found'
            success = False
        appinfo.is_continue = not appinfo.is_continue
        appinfo.save()
    result = dict(
        success=success,
        error=error
    )
    return JsonResponse(result)
