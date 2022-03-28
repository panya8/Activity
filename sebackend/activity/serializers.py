from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__' #['student_id', 'fullname']

    def to_representation(self, instance):
        result = super().to_representation(instance)       
        #result["user_data"] = UserSerializer( instance.user ).data
        return result

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'title', 'description', 'activity_type', 'userprofile', 'lecturer_name', 'is_published','day_start', 'created_at')
        read_only = ['id']
    
    def to_representation(self, instance):
        result = super().to_representation(instance)       
        result["activity_type_data"] = ActivityTypeSerializer( instance.activity_type ).data
        result["userprofile_data"] = UserProfileSerializer( instance.userprofile ).data
        return result



class ActivityTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityTimeline
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

    def to_representation(self, instance):
        result = super().to_representation(instance)       
        #result["activity_data"] = ActivitySerializer( instance.activity ).data
        result["userprofile_data"] = UserProfileSerializer( instance.userprofile ).data
        return result        

class ParticipantCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantCheckin
        fields = '__all__'

    def to_representation(self, instance):
        result = super().to_representation(instance)       
        #result["activity_data"] = ActivitySerializer( instance.activity ).data
        result["userprofile_data"] = UserProfileSerializer( instance.userprofile ).data
        return result   