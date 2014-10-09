from rest_framework import routers

from .views import (
    AppViewSet, TagViewSet, CategoryViewSet, PermissionViewSet, ScreenshotViewSet
)


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'apps', AppViewSet)
router.register(r'screenshots', ScreenshotViewSet)
