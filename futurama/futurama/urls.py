"""futurama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from subs.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', episode_index, name='index'),
    url(r'^episode/(?P<id>[0-9]+)$', episode_lines, name='episode_lines'),
    url(r'^create/(?P<id>[0-9]+)/(?P<file_format>.+)$', create_media, name='create_media'),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
