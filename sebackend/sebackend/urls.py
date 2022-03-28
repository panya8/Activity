"""sebackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers

from activity import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('userprofile', views.UserProfileViewSet)
router.register('activity', views.ActivityViewSet)
router.register('activity_type', views.ActivityTypeViewSet)
router.register('timeline', views.ActivityTimelineViewSet)
router.register('participant', views.ParticipantViewSet)
router.register('participantcheckin', views.ParticipantCheckinViewSet)

router.register('userdata', views.UserDataViewSet)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    path('v1/auth/', views.AuthView.as_view()),
    path('v1/qrcode/', views.QRCodeView.as_view()),
    path("auth/", include('rest_framework.urls', namespace='rest_framework')),

]