from django.urls import path, re_path
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.indexView, name='index'),
    #path('', auth_views.login, {'template_name':'home/index.html'}, name='index'),
    path('api-login-user/', views.LoginUserView.as_view(), name='api-login-user'),
    path('api-logout-user/', views.LogoutAPIView.as_view(), name='api-logout-user'),
    path('api-user-chat/', views.UserChatAPIView.as_view(), name='api-user-chat'),
    path('api-register-user/', views.create_user, name='api-register-user'),
    path('api-update-user-profile/<int:user__id>/', views.UserProfileUpdateAPIView.as_view(), name='api-update-user-profile'),
    path('api-service-registration/', views.ServiceRegistrationAPIView.as_view(), name='api-service-registration'),
    path('api-service-request/', views.ServiceRequestAPIView.as_view(), name='api-service-request'),
    path('api-service-request-update/<int:pk>/', views.ServiceRequestUpdateView.as_view(), name='api-service-request-update'),
    path('api-get-user-service-request/<int:id>/', views.getuserservicerequest, name='api-get-user-service-request'),
    path('search_results/', views.searchview, name='search_results'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    #path('view-profile/', views.view_profile, name='view-profile'),
    path('profile/', views.view_profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('service_registration/', views.serviceregistrationview, name='service_registration'),
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
    # Rest API from here apart from login at the top
    path('api-service/', views.ServiceView.as_view(), name='api-service'),
    path('api-get-individual-service/<int:id>/', views.individualservice, name='api-get-individual-service'),
    path('api-service-category/', views.ServiceCategoryAPIView.as_view(), name='api-service-category'),
    path('api-service-by-category/<int:id>/', views.service_by_cat, name='api-service-by-category'),
    path('api-vendor-display-by-service/<int:id>/', views.vendordisplay_by_service, name='vendor-display-by-service'),
    #re_path('profile/(?P<pk>[0-9]+)/$', views.EditProfileView.as_view(), name='edit_profile'),
    #path('user-profile/', views.user_profile, name='user_profile'),
]








