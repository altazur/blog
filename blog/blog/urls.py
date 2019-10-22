"""blog URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from blogapp import views

app_name = 'blogapp'
urlpatterns = [
    #/admin for admin panel
    url(r'^admin/', admin.site.urls),
    #/ for home page with posts
    url(r'^$', views.HomeView.as_view(), name = 'home'),
    #/1 for #1 post view
    url(r'^(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='post'),
    url(r'^createpost/$', views.create_post, name='createpost'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
