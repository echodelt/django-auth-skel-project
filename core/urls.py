"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import handler404, handler500

from .views import custom_handler404, custom_handler500

from homepage import views as homepage_views

urlpatterns = [
    url(r'^$', homepage_views.homepage, name='homepage'),
    #url(r'^errors/404$', custom_handler404, name='error-404'),
    #url(r'^errors/500$', custom_handler500, name='error-500'),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^admin/', admin.site.urls),
]

handler404 = custom_handler404
handler500 = custom_handler500
