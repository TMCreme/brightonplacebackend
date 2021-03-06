from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from braces.views import LoginRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.dispatch import receiver 
from django.forms.models import inlineformset_factory, modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import (
	UserProfile, Dialog, Message, ServiceCategory, 
	ServiceProvider, Service, MessageInbox, PostProject,
	SampleServiceDisplay,ProjectBid, ServicePackage, ClientReview,
	ServiceRegistration, ServiceRequest, FcmUserToken, VendorSample) 
from .forms import (
	RegistrationForm, UserLogin, EditProfile, UserProfileForm, 
	ServiceRegistrationForm, MessageInboxForm, PostProjectForm,
	SampleServiceDisplayForm, ProjectBidForm, ServicePackageForm)
from django.utils.safestring import mark_safe

from myproject.settings import SECRET_KEY
from django.contrib.auth import login, logout, authenticate
from .serializers import (
	UserSerializer, ServiceSerializer, ServiceCategorySerializer,
	SampleServiceDisplaySerializer, UserProfileSerializer, ServiceRegistrationSerializer,
	ServiceRequestSerializer, FcmUserTokenSerializer, VendorSampleSerializer
)
import json, os
import string
import random

# Rest framework imports for REST API for mobile side
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import jwt 

from django_rest_passwordreset.signals import reset_password_token_created

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from firebase_admin import messaging


"""
The homepage is designed to be a welcome platform. All other information that should be included in the 
basic html that have to be reflected on every page is handled in the context_processors.
TO DO: Change the menubar display at user login (may be really done in the template)
"""
def indexView(request):
	#This is handling user login since I want to include other stuff in my view
	#So I didn't use the builtin auth in the urls.
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.success(request, 'You have successfully logged in')
				return redirect('home:profile')
			else:
				messages.error(request, 'User credentials entered is not active')
				return redirect('/home')
				#print('User is None')
		else:
			messages.error(request,'User credentials entered does not exist')
			#print('User is None')
			return redirect('/home')
	user_login_form = UserLogin
		
	return render(request, 'home/index.html', {'user_login_form':user_login_form})

# REST API for login

class LoginUserView(APIView):
	
	def post(self, request, *args, **kwargs):
		username = request.data.get('username')
		password = request.data.get('password')
		
		user = authenticate(username=username, password=password)
		if user:
			myuser = User.objects.get(username=username)
			payload = jwt_payload_handler(user)
			userprofile = UserProfile.objects.get(user__id=myuser.id)
			print(request.META.get('headers'))
			up_dict = {
				'first_name': userprofile.first_name,
				'last_name':userprofile.last_name,
				'phone_number':userprofile.phone_number,
				'bio':userprofile.bio,
				'website':userprofile.website,
				'city':userprofile.city,
				'country':userprofile.country,
				'location_latitude':userprofile.location_latitude,
				'location_longitude':userprofile.location_longitude,
				'occupation':userprofile.occupation,
				'organization':userprofile.organization,
				'profile_picture':str(userprofile.profile_picture)
			}
			token = {
                'token': jwt.encode(payload, SECRET_KEY),
				'userprofile':up_dict,
                'status': 'success'
                }
			print(token)
			return Response(token)
		else:
			return Response(
              {'error': 'Invalid credentials',
              'status': 'failed'},
            )

# Password Reset 
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
	# print(reset_password_token.key)
	return Response({'status':'OK','password_reset_token':reset_password_token.key, 'email':reset_password_token.email})

# REST API LOGOUT VIEW
class LogoutAPIView(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self,request):
		print(request.user.id)
		request.data.pop('auth_token')
		try:
			FcmUserToken.objects.filter(user__id=request.user.id).delete()
		except FcmUserToken.DoesNotExist:
			pass
		return Response({'status':'success'})




class FcmUserTokenAPIView(APIView):
	def get(self, request, format=None):
		fcmtokens = FcmUserToken.objects.all()
		serializer = FcmUserTokenSerializer(fcmtokens, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = FcmUserTokenSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		print(serializer.errors)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class FcmUserTokenUpdateAPIView(APIView):
	def get_object(self, pk):
		try:
			return FcmUserToken.objects.get(pk=pk)
		except FcmUserToken.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		fcmusertoken = self.get_object(pk)
		serializer = FcmUserTokenSerializer(fcmusertoken)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		fcmusertoken = self.get_object(pk)
		serializer = FcmUserTokenSerializer(fcmusertoken, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		fcmusertoken = self.get_object(pk)
		fcmusertoken.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def send_chat_message(request, format=None):
	sender = request.data.get("sender")
	sendername = request.data.get("sendername")
	recipient = request.data.get("recipient")
	message = request.data.get("newmessage")
	print(recipient)
	try:
		registration_token = FcmUserToken.objects.get(user__id=recipient).fire_token
		print(registration_token)
		# See documentation on defining a message payload.
		message = messaging.Message(
			notification=messaging.Notification(
				title=sendername,
				body=message,
			),
			token=registration_token,
		)
		# Send a message to the device corresponding to the provided
		# registration token.
		response = messaging.send(message)
		# Response is a message ID string.
		print('Successfully sent message:', response)
		return Response({"response":response})
	except FcmUserToken.DoesNotExist:
		print("User Token does not exist")
		return Response({"response":"User Token does not exist"})
	
	
	



class UserProfileUpdateAPIView(generics.UpdateAPIView):
	parser_classes = (JSONParser, MultiPartParser, FormParser,)
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer 
	lookup_field = 'user__id'

#Service, ServiceCategory should be taken to the context processor
def serviceview(request):
	service = Service.objects.all()
	return render(request, 'home/service_search.html',)



# LIST API VIEW for Users - This view will be edited later to get only people a user has chat history with - This is done in ionic with Firebase
# Chat is stored in Firebase
class UserChatAPIView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer



@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
	serialized = UserSerializer(data=request.data)
	if serialized.is_valid():
		serialized.save()
		username = request.data.get('username') 
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
		payload = jwt_payload_handler(user)
		token = {
                'token': jwt.encode(payload, SECRET_KEY),
                'status': 'success'
                }
		return Response(token, status=status.HTTP_201_CREATED)
	else:
		return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceRegistrationAPIView(generics.ListCreateAPIView):
	queryset = ServiceRegistration.objects.all()
	serializer_class = ServiceRegistrationSerializer

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
	 return {"request":self.request}


# Service Category REST API
class ServiceCategoryAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	queryset = ServiceCategory.objects.all()
	serializer_class = ServiceCategorySerializer

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}

# Service REST API for post and get
class ServiceView(mixins.CreateModelMixin, generics.ListAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}


# Service listing by category order
class ServicebyCategoryView(generics.ListCreateAPIView):
	# queryset = ServiceCategory.objects.all()
	serializer_class = ServiceSerializer
	# lookup_url_kwarg = 'pk'

	def get_queryset(self):
		my_id = self.request.query_params.get('id')
		print(my_id)
		queryset = Service.objects.filter(servicecategory__id=my_id)
		print(queryset)
		return queryset

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}


# Vendors to be able to add samples of work and it will be displayed on their dashboard for clients
class VendorSampleView(generics.ListCreateAPIView):
	parser_classes = (JSONParser, MultiPartParser, FormParser,)
	serializer_class = VendorSampleSerializer

	def get_queryset(self):
		user_id =  self.request.query_params.get('id')
		queryset = VendorSample.objects.filter(user__id=user_id)
		return queryset

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}



# Service listing by category REST API
@api_view(['GET', 'POST'])
def service_by_cat(request,id):
	services = Service.objects.filter(servicecategory__id=id)
	serializer = ServiceSerializer(services, many=True, context={"request": request})
	return Response(serializer.data)


# Listing of Vendors according to service REST API
@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
def vendordisplay_by_service(request,id):
	services = UserProfile.objects.filter(user__id__in=Service.objects.get(id=id).serviceprovider.values_list('user__id',flat=True))
	# service_reg = ServiceRegistration.objects.get(user__id=id)
	vendor_obj = []
	for item in services:
		try:
			service_description = ServiceRegistration.objects.get(user__id=item.id, service__id=id).description 
		except ServiceRegistration.DoesNotExist:
			service_description = ""

		if item.profile_picture:
    			ppic = os.path.join(settings.STATIC_URL, str(item.profile_picture))
		else:
    			ppic = ""
		vendor_obj.append({
			"id": item.id,
			"username": item.user.username,
			"email": item.user.email,
			"profile_picture":ppic,
			"slug": item.slug,
			"first_name": item.first_name,
			"last_name": item.last_name,
			"phone_number": item.phone_number,
			"website": item.website,
			"bio": item.bio,
			"city": item.city,
			"country": item.country,
			"location_latitude": item.location_latitude,
			"location_longitude": item.location_longitude,
			"occupation": item.occupation,
			"organization": item.organization,
			"user": item.user.id,
			"service_description":service_description,
		})
	# serializer = UserProfileSerializer(services, many=True, context={"request": request})
	return Response(vendor_obj)

# Before displaying each vendor's page with their unique description of services rendered, 
# This API is for vendors to add a maximum of 5 services 
class AddSampleServiceAPI(generics.ListCreateAPIView):
    	serializer_class = SampleServiceDisplaySerializer

# Vendor's Page - After showing list of vendors, 
# This api view is for each vendor to display their sample services
@permission_classes((IsAuthenticated,))
@api_view(['GET','POST'])
def addsamplaeapiview(request):
	
	return 


@api_view(['GET'])
def individualservice(request, id):
	service = Service.objects.get(id=id)
	serialized = ServiceSerializer(service)
	return Response(serialized.data)


# This is the view for creating and getting all objects
class ServiceRequestAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	queryset = ServiceRequest.objects.all()
	serializer_class = ServiceRequestSerializer

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}


# Here is another view for update, retrive, destroy
class ServiceRequestUpdateView(generics.RetrieveUpdateDestroyAPIView):
	queryset = ServiceRequest.objects.all()
	serializer_class = ServiceRequestSerializer
	lookup_field = 'pk'



# This view collates all service request for a user - either vendor or client
@api_view(['GET'])
def getuserservicerequest(request, id):
	service_requests = ServiceRequest.objects.filter(Q(vendor__id=id) | Q(service_user__id=id))
	serializer = ServiceRequestSerializer(service_requests, many=True, context={'request':request})
	return Response(serializer.data)



#Simple sign up -- thinking of including an option to be a service provider
#In which case if user applies to be a service provider, then authentication will be deferred until approval from a SUPERUSER
#User profile is created with virtually empty params. Then when the authentication is complete, 
#the user will have the option to edit profile. Profile to include more fields.
def signup(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			user.set_password(password)
			user.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
			#login(request, user)
			if form.cleaned_data['is_service_provider'] is True:
				"""
				#TODO: Add the logic that handle the pending confirmation
				to be added to service providers
				Should send an email to the superuser/staff to be vetting
				"""
				messages.success(request,'You are signing up as a Service Provider. Complete the following...')
				return redirect('home:service_registration')

			form.save()
			"""send_mail(
                                'Welcome Message from the Team',
                                'Thank you for signing up with us. Login and update your profile',
                                settings.EMAIL_HOST_USER,
                                [email],
                                fail_silently=False,
                                )"""
			mail = EmailMessage(
                                'Welcome Message from the Team',
                                "Hi "+username+",\n Thank you for signing up with brighton.",
                                settings.EMAIL_HOST_USER,
                                [email],
                                )
			mail.send()
			messages.success(request, 'Thank you for signing up. WELCOME!!!')
			return redirect('/home')
		else:
			messages.error(request, 'Sorry, Form validation failed. Try refreshing the page and re-submit credentials to join')
			#print(form.errors)
	else:
		form = RegistrationForm()
	return render(request, 'home/reg_form.html', {'form':form})

def serviceregistrationview(request):
	service_form = ServiceRegistrationForm
	serv = Service.objects.all()
	current_user = User.objects.get(username=request.user)
	email = current_user.email
	if request.method == 'POST':
		service_form = ServiceRegistrationForm(request.POST)
		if service_form.is_valid():
			cd = service_form.cleaned_data
			serv_category = cd['service_category']
			serv_reg = cd['service']
			print(serv_reg)
			#Send the email confirmation to the user and self including the services chosen
			#service_form.save()
			mail = EmailMessage(
					'Welcome Message from the Team',
					"Hi "+current_user.username+", Thank you for signing up with brighton. We also acknowledge your request to be a service provider. Your request is for the following service(s): "+str(serv_reg) + ", under "+serv_category+ " category. Your credentials will be vetted and response communicated to you as soon as possible. Should we require additional information, we will contact you. Thanks once again.",
					settings.EMAIL_HOST_USER,
                    [email, settings.EMAIL_HOST_USER],
					)
			mail.send()
			messages.success(request,'You have successfully applied for service provider status. Your credentials will be vetted and feedback sent to you by email.')
			return redirect('home:profile')
		else:
			print(service_form)
			messages.error(request, 'Sorry, Form validation failed.')
	args = {'serv':serv, 'service_form':service_form}
	return render(request, 'home/service_reg.html', args)

#Nothing fancy about the logout view. Simple
def LogoutView(request):
	messages.info(request, "You have logged out. Please log in to have full access")
	return redirect('/home')

"""
This will have the option of pending the authentication of service providers.
"""

#The login required decorator is needed cos you need to login to see and edit your profile
@login_required
def edit_profile(request):
	#First, get the loggged-in userprofile and put the field content in a dictionary
	user = UserProfile.objects.get(user__username=request.user)
	user_dict = {
		'phone_number':user.phone_number,
		'bio':user.bio,
		'website':user.website,
		'city':user.city,
		'country':user.country,
		'organization':user.organization,
		'profile_picture':user.profile_picture,
		'occupation':user.occupation,
		}
	#This form is called with the initial values been the existing profile contents of the user 
	user_form = EditProfile(initial={'first_name':request.user.first_name,'last_name':request.user.last_name})
	form = UserProfileForm(initial=user_dict)
	#Now if it is a POST request, the form updating logic is here
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES)
		user_form = EditProfile(request.POST, instance=request.user)
		#Now check the validation
		if user_form.is_valid():
			user_form.save(commit=False)
			if form.is_valid():
				#Call (by filter) the userprofile for updating
				user_update = UserProfile.objects.get(user__username=request.user)
				#Use the cleaned data of the form to update 
				user_update.phone_number = form.cleaned_data['phone_number']
				user_update.bio = form.cleaned_data['bio']
				user_update.website = form.cleaned_data['website']
				user_update.city = form.cleaned_data['city']
				user_update.country = form.cleaned_data['country']
				user_update.organization = form.cleaned_data['organization']
				user_update.occupation = form.cleaned_data['occupation']
				user_update.profile_picture = request.FILES.get('profile_picture', user.profile_picture)
				user_update.save()
				user_form.save()
				#After updating, redirect to the user profile page
				messages.success(request, 'You have successfully updated your profile. Thank you.')
				return redirect('home:profile')
			else:
				messages.error(request,'Form validation failed. Try again later.')
				return redirect('home:profile')
		else:
			messages.error(request,'Form validation failed. Try again later.')
			return redirect('home:profile')
	return render(request, 'home/edit_profile.html', {'form':form,'user_form':user_form})


#Nothin fancy going on here. The real deal is to redesign the frontend for better UX
@login_required
def view_profile(request):
	users = User.objects.all()
	up = UserProfile.objects.get(user__username=request.user)
	usp = UserProfile.objects.all()
	user_service = Service.objects.filter(serviceprovider__user__username=request.user)
	#sampleprojs = get_object_or_404(SampleServiceDisplay, user__username=request.user)
	#if ServiceProvider.objects.filter(user__username=request.user):
	user_projects = PostProject.objects.filter(client__username=request.user)
	sampleprojs = SampleServiceDisplay.objects.filter(user__username=request.user)
	client_review = ClientReview.objects.filter(serviceprovider__user__username=request.user)
	logged_user = request.user
	mesages = MessageInbox.objects.filter(Q(fromUser=logged_user) | Q(toUser=logged_user)).order_by('-createdAt')
	args = {'user':request.user, 'users':users, 'usp':usp, 'up':up,'sampleprojs':sampleprojs, 'user_service':user_service, 'mesages':mesages, 'user_projects':user_projects, 'client_review':client_review}
	#print(request.u.city)
	return render(request, 'home/view_profile.html', args)

#This is concerning the chat side. Really not being used at all at the moment
def room(request, room_name):
	return render(request, 'home/view_profile.html', {
		'room_name_json':mark_safe(json.dumps(room_name))
	})


"""
#This can be used to browse other users dashboard to see what they have:
if they are service providers, then their services will be listed on 
their respective pages
"""
def userdashboard(request, id):
	resulted_user = User.objects.get(id=id)
	resulted_user_profile = UserProfile.objects.get(user__username=resulted_user)
	service_package = ServicePackage.objects.filter(serviceprovider__user__username=resulted_user)[:3]
	resulted_user_service = PostProject.objects.filter(serviceprovider__user__username=resulted_user, completed=True)[:5]
	sample_work = SampleServiceDisplay.objects.filter(user__username=resulted_user)
	args = {'resulted_user':resulted_user,'resulted_user_profile':resulted_user_profile,'service_package':service_package, 'resulted_user_service':resulted_user_service, 'sample_work':sample_work}
	return render(request, 'home/user_dashboard.html', args)

#For sending message to other users
@login_required
def sendmessageview(request, id):
	receiving_user = User.objects.get(id=id)
	message_form = MessageInboxForm(initial={'fromUser':request.user, 'toUser':receiving_user})
	if request.method == 'POST':
		message_form = MessageInboxForm(request.POST)
		if message_form.is_valid():
			subject = message_form.cleaned_data['subject']
			email = receiving_user.email
			message = message_form.cleaned_data['message']
			image = message_form.cleaned_data['image']
			#Clean the form data and send email
			message_form.save()
			mail = EmailMessage(
				'You have a message with the subject: '+subject,
				"Hi "+receiving_user+",\n "+request.user+" sent you a message. Please find below the message. \n"+message,
                settings.EMAIL_HOST_USER,
                [email],
				)
			mail.attach(image.name, image.read(), image.content_type)
			mail.send()
			messages.success(request,'Your message has been sent. We will notify you as soon as there is a reply.')
			return redirect('home:profile')
		else:
			messages.error(request, 'Form validation failed. Please try again later')

	args = {'message_form':message_form, 'receiving_user':receiving_user}
	return render(request, 'home/send_message.html', args)

@login_required
def inboxview(request):
	logged_user = request.user
	mesages = MessageInbox.objects.filter(Q(fromUser=logged_user) | Q(toUser=logged_user)).order_by('-createdAt')
	args = {'mesages':mesages}
	return render(request, 'home/inbox.html', args)

#For posting jobs so service providers can bid on
@login_required
def postprojectview(request):
	postproject_form = PostProjectForm(initial={'client':request.user})
	if request.method == 'POST':
		postproject_form = PostProjectForm(request.POST, request.FILES)
		if postproject_form.is_valid():
			#category = Service.objects.get(servicecategory__name=postproject_form.cleaned_data['category'])
			#postproject_form.cleaned_data['category'] = category
			print(postproject_form.cleaned_data['category'])
			#Clean the form and send a notifiction to all service providers listed under the particular service.
			postproject_form.save()
			messages.success(request,'You have successfully posted a project. We will notify you as and when bids are placed.')
			return redirect('home:profile')
		else:
			messages.error(request,'Form validation failed. Please try again later.')
			return redirect('home:profile')
	args = {'postproject_form':postproject_form}

	return render(request, 'home/postproject.html', args)



#For those service providers that want to display their work
@login_required
def sampleprojectdisplayview(request):
	data = {'user':request.user}
	sampleproject_form = SampleServiceDisplayForm(initial={'user':request.user})
	if request.method == 'POST':
		sampleproject_form = SampleServiceDisplayForm(request.POST, request.FILES)
		#TODO: Add the logic that allows only service_providers
		if ServiceProvider.objects.filter(user=request.user).exists():
			if sampleproject_form.is_valid():
				sampleproject_form.save()
				messages.success(request,'You have successfully posted a a sample to be displayed on your dashboard for client so see.')
				return redirect('home:profile')
			else:
				messages.error(request,'Sorry, something went wrong and your project was not saved. Please try again later.')
				return redirect('home:profile')
		else:
			#Display message that only service providers can post samples
			messages.info(request,'Only those with a service Provider status can post their sample works to attract customers. If you wish to post a work to be done for you, select post a project and receive competitive bids from professionals.')
			return redirect('home:profile')
	args = {'sampleproject_form':sampleproject_form}
	return render(request, 'home/sample_display.html', args)

#This is to display all of the service provider's samples
def serviceview(request, slug):
	servicepage = SampleServiceDisplay.objects.filter(service__slug=slug)
	#user_profile = Service.objects.filter(name=slug).values_list()
	args = {'servicepage':servicepage, 'slug':slug}
	return render(request, 'home/service_page.html', args)

#This is to show the detail of a sample that's selected from the list of services displayed
def SampleServiceDetailView(request, id):
	servicesample = SampleServiceDisplay.objects.get(id=id)
	args = {'servicesample':servicesample}
	return render(request, 'home/sample_display_detail.html', args)

#This is to display all services under a category when the user requests a category
def ServiceCategoryView(request, slug):
	sercatlist = Service.objects.filter(servicecategory__slug=slug)#There's a p here with the name
	args = {'sercatlist':sercatlist, 'slug':slug}
	return render(request, 'home/serv_category.html', args)

@login_required
def postedprojectlist(request):
	my_user = PostProject.objects.filter(service__serviceprovider__user__username=request.user)
	args = {'my_user':my_user}
	return render(request, 'home/project_list.html', args)

@login_required
def postedprojectview(request, id):
	posted_project = PostProject.objects.get(id=id)
	existing_bids = ProjectBid.objects.filter(project__id=id)
	reference = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
	bid_form_initial = {
	'bid_reference':reference,
	'project':posted_project,
	'bidder':ServiceProvider.objects.get(user__username=request.user.username),
	'client':posted_project.client,
	'service':posted_project.service,
	}
	projectbid_form = ProjectBidForm(initial=bid_form_initial)
	if request.method == 'POST':
		projectbid_form = ProjectBidForm(request.POST)
		if projectbid_form.is_valid():
			projectbid_form.save()
			messages.success(request, 'Your BID has been placed successfully placed. If your bid is selected by the client, we will contact you.')
			return redirect('home:profile')
		else:
			messages.error(request,'Your bid was not placed due to Form validation failure. Please try again later.')
			print(projectbid_form.errors)
	args = {'posted_project':posted_project, 'projectbid_form':projectbid_form,'existing_bids':existing_bids}
	return render(request, 'home/posted_project.html', args)

#Take this to the project display page and make the form a popup or something else. Then include an initial arg for bid_reference, project
@login_required
def projectbidview(request):
	projectbid_form = ProjectBidForm(request.POST)
	if request.method == 'POST':
		projectbid_form = ProjectBidForm(request.POST)
		if projectbid_form.is_valid():
			projectbid_form.save()
			messages.success(request, 'Your BID has been placed successfully placed. If your bid is selected by the client, we will contact you.')
			return redirect('home:profile')
		else:
			messages.error(request,'Your bid was not placed due to Form validation failure. Please try again later.')
	args = {'projectbid_form':projectbid_form}
	return render(request, 'home/projectbidding.html', args)



def searchview(request):
	query = request.GET.get('q')
	results = SampleServiceDisplay.objects.filter(Q(service__name__icontains=query) | Q(servicecategory__name__icontains=query))
	print(query)
	args = {'results':results}
	return render(request, 'home/search_results.html', args)

























"""
def UserLoginView(request):
	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/home')

	else:
		form = UserLogin()
		return render(request, 'home/index.html', {'form':form})"""



# Create your views here.
