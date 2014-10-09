from rest_framework.serializers import HyperlinkedModelSerializer

from store.models import (
    AppInfo, Category, Screenshot
)


class AppSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AppInfo


class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category


class ScreenshotSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Screenshot
