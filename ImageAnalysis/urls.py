"""ImageAnalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import url
 
from . import view
 
urlpatterns = [
    url(r'^$', view.hello),
    url(r'upload_file$',view.upload_file),
    url(r'page_1$',view.page_1),
    url(r'page_2$',view.page_2),
    url(r'page_3$',view.page_3),
    url(r'img_num$',view.img_num), 
    url(r'img_class$',view.img_class), 
    url(r'search_file$',view.search_file), 
    url(r'recognize$',view.recognize), 
]