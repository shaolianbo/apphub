from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField

from store.models import (
    AppInfo, Category, Screenshot
)


class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category


class AppSerializer(HyperlinkedModelSerializer):
    category = SerializerMethodField('get_category_name')
    tags = SerializerMethodField('get_tags_names')
    screen_shots = SerializerMethodField('get_screen_shots')
    app_id = SerializerMethodField('get_apk_name')

    class Meta:
        model = AppInfo

    def get_category_name(self, obj):
        return obj.category.name

    def get_tags_names(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_screen_shots(self, obj):
        return obj.screenshot_set.all().values('image', 'origin_url')

    def get_apk_name(self, obj):
        return obj.app_id.apk_name


class ScreenshotSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Screenshot
