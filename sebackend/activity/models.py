from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=False, blank=True, null=True, on_delete=models.CASCADE)

    profile_type = models.CharField(max_length=16, default='member', null=False)
    member_id = models.CharField(max_length=12, null=False)
    
    fullname = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.CharField(max_length=50, blank=True, null=True)
    contract = models.CharField(max_length=12, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)

    password = models.CharField(max_length=16, blank=True, null=False)

    def __str__(self):
        return self.member_id + " " + self.fullname

class ActivityType(models.Model):
    activity_type_name = models.CharField(unique=True, max_length=50)
    activity_type_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.activity_type_name

class Activity(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=255,blank=True, null=True)
    activity_type = models.ForeignKey(ActivityType, unique=False, on_delete=models.CASCADE)
    lecturer_name = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    day_start = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    userprofile = models.ForeignKey(UserProfile, unique=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ActivityTimeline(models.Model):
    activity = models.ForeignKey(Activity, unique=False, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    lecturer_name = models.CharField(max_length=50, blank=True, null=True)
    start_datetime_text = models.CharField(max_length=50, blank=True, null=True)
    end_datetime_text = models.CharField(max_length=50, blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    timeline_day = models.IntegerField(default=1)

    def __str__(self):
        return self.description



class Participant(models.Model):
    activity = models.ForeignKey(Activity, unique=False, on_delete=models.CASCADE)
    userprofile = models.ForeignKey(UserProfile, unique=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'userprofile')

    def __str__(self):
        return self.activity 


class ParticipantCheckin(models.Model):
    activity = models.ForeignKey(Activity, unique=False, on_delete=models.CASCADE)
    userprofile = models.ForeignKey(UserProfile, unique=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'userprofile')

    def __str__(self):
        return self.activity

