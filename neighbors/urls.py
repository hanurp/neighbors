"""neighbors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]
if 'rest_framework' in settings.INSTALLED_APPS:
    from person.views import PersonViewSet, person_search_nearby
    from rest_framework import routers
    router = routers.DefaultRouter()
    router.register(r'persons', PersonViewSet)
    urlpatterns = [
        path(r'persons/nearby/', person_search_nearby),
        path(r'', include(router.urls)),
    ]