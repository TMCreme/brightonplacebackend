from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.indexView, name='index'),
    #path('', auth_views.login, {'template_name':'home/index.html'}, name='index'),
"""    path('search_results/', views.searchview, name='search_results'),
    path('logout/', views.LogoutView, name='logout'),
    path('signup/', views.signup, name='signup'),
    #path('view-profile/', views.view_profile, name='view-profile'),
    path('profile/', views.view_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('service_registration/', views.serviceregistration, name='service_registration'),
    path('userdashboard/<int:id>/', views.userdashboard, name='userdashboard'),
    path('sendmessage/<int:id>/', views.sendmessageview, name='sendmessage'),
    path('inbox/', views.inboxview, name='inbox'),
    path('postproject/', views.postprojectview, name='postproject'),
    path('sample_project_display/', views.sampleprojectdisplayview, name='sample_project_display'),
    path('postedsample/<int:id>/', views.SampleServiceDetailView, name='postedsample'),
    path('servicecategory/<slug:slug>/', views.ServiceCategoryView, name='servicecategory'),
    path('service_result_page/<slug:slug>/', views.serviceview, name='service_result_page'),
    path('postedproject/<int:id>/', views.postedprojectview, name='postedproject'),
    path('postprojectlist/', views.postedprojectlist, name='postprojectlist'),
    path('projectbid/', views.projectbidview, name='projectbid'),
    #re_path('profile/(?P<pk>[0-9]+)/$', views.EditProfileView.as_view(), name='edit_profile'),
    #path('user-profile/', views.user_profile, name='user_profile'),"""
]

"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""




