from rest_framework import routers

from django.urls import path

from bcmr import views


app_name = "bcmr"

router = routers.DefaultRouter()

router.register("registries", views.RegistryViewSet)
router.register("tokens", views.TokenViewSet)

urlpatterns = router.urls + [
    path('create_token/fungible/', views.create_token)
]
