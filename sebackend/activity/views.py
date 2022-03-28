from django.conf import settings
from django.db.models import query
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView 
from django.contrib.auth.models import User, Group
from .models import *
from .serializers import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def list(self, request):
        queryset = Activity.objects.all().order_by('-created_at')

        userprofile = request.GET.get('userprofile', None)
        if (not userprofile is None):
            queryset = queryset.filter(userprofile=userprofile)

        is_published = request.GET.get('is_published', None)
        if (not is_published is None):

            if (is_published == "true"):
                is_published = True
            else:
                is_published = False
            queryset = queryset.filter(is_published=is_published)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ActivityTypeViewSet(viewsets.ModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer

class ActivityTimelineViewSet(viewsets.ModelViewSet):
    queryset = ActivityTimeline.objects.all()
    serializer_class = ActivityTimelineSerializer

    def list(self, request):
        queryset = ActivityTimeline.objects.all()
        
        activity = request.GET.get('activity', None)
        if (not activity is None):
            queryset = queryset.filter(activity=activity)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def list(self, request):
        queryset = Participant.objects.all()
        
        activity = request.GET.get('activity', None)
        if (not activity is None):
            queryset = queryset.filter(activity=activity)
        userprofile = request.GET.get('userprofile', None)
        if (not userprofile is None):
            queryset = queryset.filter(userprofile=userprofile)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ParticipantCheckinViewSet(viewsets.ModelViewSet):
    queryset = ParticipantCheckin.objects.all()
    serializer_class = ParticipantCheckinSerializer

    def list(self, request):
        queryset = ParticipantCheckin.objects.all()
        
        activity = request.GET.get('activity', None)
        if (not activity is None):
            queryset = queryset.filter(activity=activity)
        userprofile = request.GET.get('userprofile', None)
        if (not userprofile is None):
            queryset = queryset.filter(userprofile=userprofile)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

##True if getattr(settings, "TIMEZONE_TZ", None) else exit()



# Custom User Authen
import json
class AuthView(APIView):
    queryset = UserProfile.objects.all()

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if (username is None and password is None):
            inputs = request.data
            if (not inputs is None):
                username = inputs['username']
                password = inputs['password']

        data = { "success": False }
        if (not username is None and not password is None):
            #user = User.objects.get(username=username)
            #if (not user is None and user.check_password(password)):
            user = UserProfile.objects.get(member_id__exact=username, password__exact=password)
            if (not user is None):
                token = user.id
                data = { 
                    "success": True, 
                    "data": UserProfileSerializer(user, many=False).data,                    
                    "token": token 
                }
        
        return Response(data)

# Current User Data Provider for Custom User Authen
class UserDataViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request):        
        return Response({})    

    def create(self, request):
        token = request.POST.get('token', None)
        if (not token is None):
            queryset = UserProfile.objects.get(user=token, )
            serializer = self.get_serializer(queryset, many=False)
            return Response(serializer.data)    
        return Response({})    

    def retrieve(self, request, pk=None):
        return Response({})    

    def update(self, request, pk=None):
        return Response({})    

    def partial_update(self, request, pk=None):
        return Response({})    

    def destroy(self, request, pk=None):
        return Response({})  


# QRCode Image Response View
import qrcode
from django.http import HttpResponse

class QRCodeView(APIView):
    def get(self, request, format=None):
        url = request.GET.get('url', None)
        if (not url is None):
            q = qrcode.QRCode(
                box_size=5,
                version=5,
                error_correction=qrcode.constants.ERROR_CORRECT_L,            
                border=4,
            )
            q.add_data(url)
            q.make(fit=True)
            img = q.make_image(fill_color="black", back_color="white")
            response = HttpResponse(content_type='image/png')
            img.save(response, "png")
            return response

        return Response({ "success": False, "error": "Invalid Request." }, 403)
