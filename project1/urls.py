"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
    path('Signup/', views.sign_up, name='signup'),
    path('Login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='log_out'),
    path('smm/', views.smm, name='smm'),
    path('pricing/', views.pricing, name='pricing'),
    path('profile/',views.profile,name='profile'),
    path('Signup/Login',views.log_in, name='login'),
    path('profile/uploadadd/', views.uploadadd, name='uploadadd'),
    path('profile/yourads/', views.yourads, name='yourads'),
    path('iprofile/',views.iprofile,name='iprofile'),
    path('iprofile/yourads/', views.iyouradds, name='iyouradds'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)