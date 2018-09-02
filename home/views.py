"""from django.shortcuts import render, redirect, get_object_or_404 
from braces.views import LoginRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms.models import inlineformset_factory, modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
	UserProfile, Dialog, Message, ServiceCategory, 
	ServiceProvider, Service, MessageInbox, PostProject,
	SampleServiceDisplay,ProjectBid, ServicePackage) 
from .forms import (
	RegistrationForm, UserLogin, EditProfile, UserProfileForm, 
	ServiceRegistration, MessageInboxForm, PostProjectForm,
	SampleServiceDisplayForm, ProjectBidForm, ServicePackageForm)
from django.utils.safestring import mark_safe
import json
import string
import random


"""
"""
The homepage is designed to be a welcome platform. All other information that should be included in the 
basic html that have to be reflected on every page is handled in the context_processors.
TO DO: Change the menubar display at user login (may be really done in the template)
"""
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

#Service, ServiceCategory should be taken to the context processor
def serviceview(request):
	service = Service.objects.all()
	return render(request, 'home/service_search.html',)

#Simple sign up -- thinking of including an option to be a service provider
#In which case if user applies to be a service provider, then authentication will be deferred until approval from a SUPERUSER
#User profile is created with virtually empty params. Then when the authentication is complete, 
#the user will have the option to edit profile. Profile to include more fields.
def signup(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			if form.cleaned_data['is_service_provider'] is True:
				"""
"""
				#TODO: Add the logic that handle the pending confirmation
				to be added to service providers
				Should send an email to the superuser/staff to be vetting
				""""""
				form.save()
				messages.success(request,'You are signing up as a Service Provider. Complete the following...')
				return redirect('home:service_registration')

			form.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, 'Thank you for signing up. WELCOME!!!')
			return redirect('/home/profile')
		else:
			messages.error(request, 'Sorry, Form validation failed. Try refreshing the page and re-submit credentials to join')
			#print('Form is not valid')
	else:
		form = RegistrationForm()
		return render(request, 'home/reg_form.html', {'form':form})

def serviceregistration(request):
	service_form = ServiceRegistration
	serv = Service.objects.all()
	if request.method == 'POST':
		service_form = ServiceRegistration(request.POST)
		if service_form.is_valid():
			cd = service_form.cleaned_data
			serv_category = cd['service_category']
			serv_reg = cd['service']
			print(serv_reg)
			#service_form.save()
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
	"""
This will have the option of pending the authentication of service providers.
"""
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
				user_update = UserProfile.objects.filter(user__username=request.user)
				#Use the cleaned data of the form to update 
				user_update.update(phone_number=form.cleaned_data['phone_number'])
				user_update.update(bio=form.cleaned_data['bio'])
				user_update.update(website=form.cleaned_data['website'])
				user_update.update(city=form.cleaned_data['city'])
				user_update.update(country=form.cleaned_data['country'])
				user_update.update(organization=form.cleaned_data['organization'])
				user_update.update(occupation=form.cleaned_data['occupation'])
				if form.cleaned_data['profile_picture']:
					user_update.update(profile_picture=form.cleaned_data['profile_picture'])
				else:
					user_update.update(profile_picture=user.profile_picture)
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
	sampleprojs = SampleServiceDisplay.objects.filter(user__user__username=request.user)
	logged_user = request.user
	mesages = MessageInbox.objects.filter(Q(fromUser=logged_user) | Q(toUser=logged_user)).order_by('-createdAt')
	args = {'user':request.user, 'users':users, 'usp':usp, 'up':up,'sampleprojs':sampleprojs, 'user_service':user_service, 'mesages':mesages, 'user_projects':user_projects}
	#print(request.u.city)
	return render(request, 'home/view_profile.html', args)

#This is concerning the chat side. Really not being used at all at the moment
def room(request, room_name):
	return render(request, 'home/view_profile.html', {
		'room_name_json':mark_safe(json.dumps(room_name))
	})


"""'
"""
#This can be used to browse other users dashboard to see what they have:
if they are service providers, then their services will be listed on 
their respective pages
"""
"""
def userdashboard(request, id):
	resulted_user = User.objects.get(id=id)
	resulted_user_profile = UserProfile.objects.get(user__username=resulted_user)
	service_package = ServicePackage.objects.filter(serviceprovider__user__username=resulted_user)[:3]
	resulted_user_service = PostProject.objects.filter(serviceprovider__user__username=resulted_user, completed=True)[:5]
	args = {'resulted_user':resulted_user,'resulted_user_profile':resulted_user_profile,'service_package':service_package, 'resulted_user_service':resulted_user_service}
	return render(request, 'home/user_dashboard.html', args)

#For sending message to other users
@login_required
def sendmessageview(request, id):
	receiving_user = User.objects.get(id=id)
	message_form = MessageInboxForm(initial={'fromUser':request.user, 'toUser':receiving_user})
	if request.method == 'POST':
		message_form = MessageInboxForm(request.POST)
		if message_form.is_valid():
			#Clean the form data and send email
			message_form.save()
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
			category = Service.objects.get(servicecategory__name=postproject_form.cleaned_data['service'])
			postproject_form.cleaned_data['category'] = category
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
	reference = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
	bid_form_initial = {
	'bid_reference':reference,
	'project':posted_project,
	'bidder':request.user,
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
	args = {'posted_project':posted_project, 'projectbid_form':projectbid_form}
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

def indexView(request):
        return

# Create your views here.
