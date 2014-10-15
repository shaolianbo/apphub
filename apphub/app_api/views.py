from rest_framework import viewsets

from store.models import (
    AppInfo, Tag, Category, Permission, Screenshot, AppIdentification
)
from .serializers import AppSerializer, CategorySerializer, ScreenshotSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    model = Tag


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    model = Permission


class AppIdentificationViewSet(viewsets.ReadOnlyModelViewSet):
    model = AppIdentification

    def get_queryset(self):
        queryset = AppIdentification.objects.all()
        apk_name = self.request.QUERY_PARAMS.get('apk_name', None)
        if apk_name:
            queryset = queryset.filter(apk_name=apk_name)
        return queryset


class AppViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppInfo.objects.all()
    serializer_class = AppSerializer

    def get_queryset(self):
        queryset = AppInfo.objects.all()
        apk_name = self.request.QUERY_PARAMS.get('apk_name', None)
        if apk_name:
            queryset = queryset.filter(app_id__apk_name=apk_name)
        return queryset


class ScreenshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
