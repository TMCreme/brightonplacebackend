from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
	UserProfile, ServiceCategory, ServiceProvider, Service, MessageInbox,
	PostProject, SampleServiceDisplay, ProjectBid, ServicePackage, ClientReview, UserLocation)
#from .forms import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user','organization','website','city']

admin.site.register(UserProfile,UserProfileAdmin)

from django.contrib.sessions.models import Session
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

class ServiceAdmin(admin.ModelAdmin):
	list_display = ['name', 'servicecategory',]
	prepopulated_fields = {'slug':('name',)}
admin.site.register(Service, ServiceAdmin)

class ServiceCategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug']
	prepopulated_fields = {'slug':('name',)}
admin.site.register(ServiceCategory, ServiceCategoryAdmin)

class ServiceProviderAdmin(admin.ModelAdmin):
	list_display = ['user']
admin.site.register(ServiceProvider, ServiceProviderAdmin)


class MessageInboxAdmin(admin.ModelAdmin):
	list_display = ['createdAt','fromUser','toUser','subject','message']
	prepopulated_fields = {'slug':('fromUser',)}
admin.site.register(MessageInbox, MessageInboxAdmin)

class PostProjectAdmin(admin.ModelAdmin):
	list_display = ['client','title','category','service','description','other_information']
admin.site.register(PostProject, PostProjectAdmin)

class SampleServiceDisplayAdmin(admin.ModelAdmin):
	list_display = ['user','servicecategory','service','search_tags']
admin.site.register(SampleServiceDisplay)

class ProjectBidAdmin(admin.ModelAdmin):
	list_display = ['bid_reference','project','description','cost','commission']
admin.site.register(ProjectBid, ProjectBidAdmin)


class ServicePackageAdmin(admin.ModelAdmin):
	list_display = ['name','serviceprovider','service','cost','delivery_timeline']
admin.site.register(ServicePackage, ServicePackageAdmin)


class ClientReviewAdmin(admin.ModelAdmin):
	list_display = ['user','serviceprovider','service','transaction_id','review']
admin.site.register(ClientReview, ClientReviewAdmin)


admin.site.register(UserLocation)









# Register your models here.


