from django.contrib import admin
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    pass

class ActivityTypeAdmin(admin.ModelAdmin):
    pass

class ActivityAdmin(admin.ModelAdmin):
    pass

class ActivityTimelineAdmin(admin.ModelAdmin):
    pass

class ParticipantAdmin(admin.ModelAdmin):
    pass

class ParticipantCheckinAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityType, ActivityTypeAdmin)
admin.site.register(ActivityTimeline, ActivityTimelineAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(ParticipantCheckin, ParticipantCheckinAdmin)