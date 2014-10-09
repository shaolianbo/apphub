from rest_framework import viewsets

from store.models import (
    AppInfo, Tag, Category, Permission, Screenshot
)
from .serializers import AppSerializer, CategorySerializer, ScreenshotSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    model = Tag


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    model = Permission


class AppViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppInfo.objects.all()
    serializer_class = AppSerializer


class ScreenshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
