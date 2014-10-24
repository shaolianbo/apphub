from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField

from store.models import (
    AppInfo, Category, Screenshot
)


class CategorySerializer(HyperlinkedModelSerializer):
    tags = SerializerMethodField('get_tags')

    def get_tags(self, obj):
        return [tag[0] for tag in obj.tags.all()[:10].values_list('name')]

    class Meta:
        model = Category
        fields = ['name', 'top_type', 'tags']


class AppSerializer(HyperlinkedModelSerializer):
    category = SerializerMethodField('get_category_name')
    tags = SerializerMethodField('get_tags_names')
    screen_shots = SerializerMethodField('get_screen_shots')
    app_id = SerializerMethodField('get_apk_name')
    top_type = SerializerMethodField('get_top_type')

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

    def get_top_type(self, obj):
        return obj.app_id.top_type


class ScreenshotSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Screenshot
