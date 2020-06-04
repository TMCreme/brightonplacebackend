from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from .models import (
	UserProfile, Service, ClientReview,
	ServiceCategory,ServiceProvider, Transaction,
	MessageInbox, PostProject, SampleServiceDisplay, ProjectBid, ServicePackage)
import json


class RegistrationForm(UserCreationForm):
	email = forms.EmailField()
	is_service_provider = forms.BooleanField(required=False)
	
	class Meta:
		model = User
		fields = [
		'username',
		'email',
		'password1',
		'password2',
		'is_service_provider',
		]

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user

class EditProfile(UserChangeForm):
	class Meta:
		model = User
		fields =[
		'first_name',
		'last_name',
		'password',
		]

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = [
		'phone_number',
		'bio',
		'website',
		'city',
		'country',
		'occupation',
		'organization',
		'profile_picture',
		]

class UserLogin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =['username', 'password']


class ServiceRegistrationForm(forms.Form):
	catt_list = []
	catt_dict = {}
	serv_list = []
	serv_dict = {}
	cattt = ServiceCategory.objects.all()
	servv = Service.objects.all()
	for name in cattt:
		catt_list.append(name.name)
		serv_dict[name.name] = []
	for m in servv:
		serv_list.append(m.name)
		#catt_dict[m.servicecategory.name].append(m.name)
	for namm in catt_list:
		for nam in servv:
			if namm not in catt_dict and nam.servicecategory.name == namm:
				catt_dict[namm] = [nam.name]
			elif namm in catt_dict and nam.servicecategory.name == namm:
				catt_dict[namm].append(nam.name)

	categ = json.dumps(catt_list)
	servcat = json.dumps(catt_dict)
	servlist = json.dumps(serv_list)
	

	service_category = forms.ChoiceField(choices=([(cat, cat) for cat in catt_list]))
	service = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=([(serv,serv) for serv in serv_list]))

	class Meta:
		#model = ServiceProvider
		fields = ['service_category', 'service']


class MessageInboxForm(forms.ModelForm):

	class Meta:
		model = MessageInbox
		fields = ['fromUser','toUser','subject','message','image']


class PostProjectForm(forms.ModelForm):

	class Meta:
		model = PostProject
		fields = ['client','title','category','service',
		'description','other_information','image']


class SampleServiceDisplayForm(forms.ModelForm):

	class Meta:
		model = SampleServiceDisplay
		fields = ['user','servicecategory','service',
		'search_tags','description','sample_image']


class ProjectBidForm(forms.ModelForm):
	commission = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	total_cost = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

	class Meta:
		model = ProjectBid
		fields = ['project','cost','commission','bid_reference','description','bidder','client','service', 'total_cost']


class ServicePackageForm(forms.ModelForm):

	class Meta:
		model = ServicePackage
		fields = ['serviceprovider','service','name','detail', 'delivery_timeline','cost','description']


class ClientReviewForm(forms.ModelForm):

	class Meta:
		model = ClientReview
		fields = ['user','serviceprovider','service','transaction_id','review',]



