from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime
from django.conf import settings
import string
import random


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=250,db_index=True)
	first_name = models.CharField(max_length=250, blank=True, null=True)
	last_name = models.CharField(max_length=250, blank=True, null=True)
	phone_number = models.CharField(max_length=250, blank=True, null=True)
	website = models.URLField(default='', blank=True)
	bio = models.TextField(default='', blank=True)
	city = models.CharField(max_length=300, default='', blank=True)
	country = models.CharField(max_length=250, default='', blank=True)
	location_latitude = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
	location_longitude = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
	occupation = models.CharField(max_length=300, default='', blank=True)
	organization = models.CharField(max_length=300, default='',blank=True)
	profile_picture = models.ImageField(upload_to='home', blank=True, null=True)

	def __unicode__(self):
		return self.user

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class FcmUserToken(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	fire_token = models.CharField(max_length=500)

# def create_fcmtoken(sender, **kwargs):
# 	if kwargs['created']:
# 		fcm_usertoken = FcmUserToken.objects.create(user)

class UserLocation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	region = models.CharField(max_length=250, null=True, blank=True)
	district = models.CharField(max_length=250, null=True, blank=True)
	locality = models.CharField(max_length=250, null=True, blank=True)
	latitude = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
	longitude = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)


class ServiceCategory(models.Model):
	name = models.CharField(max_length=250, db_index=True)
	slug = models.SlugField(max_length=250, db_index=True, unique=True)
	image = models.ImageField(blank=True, upload_to='home')

	class Meta:
		ordering = ('name',)
		verbose_name = 'servicecategory'
		verbose_name_plural = 'servicecategories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home:servicecategory', args=[self.slug])

class ServiceProvider(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.user.username
	

class Service(models.Model):
	servicecategory = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
	serviceprovider = models.ManyToManyField(ServiceProvider, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, db_index=True)
	description = models.TextField()
	sample_image = models.ImageField(blank=True, null=True, upload_to='home')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)

	

	def get_absolute_url(self):
		return reverse('home:detail', args=[self.id, self.slug])


# New model for service registration. 
class ServiceRegistration(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	servicecategory = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
	service = models.ManyToManyField(Service)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.user.username


#Handle if message is not deliverd, sent a feedback to sender and inlcude staff support contact option
class MessageInbox(models.Model):
	fromUser = models.ForeignKey(User, related_name='fromUser', on_delete=models.CASCADE)
	toUser = models.ForeignKey(User, related_name='toUser', on_delete=models.CASCADE)
	slug = models.SlugField(max_length=250, db_index=True)
	subject = models.CharField(max_length=500)
	message = models.TextField()
	image = models.ImageField(blank=True)
	createdAt = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.subject +'. from '+ self.fromUser.username
#Query for messages -> messages = Message.objects.order_by('fromUser','toUser','createdAt').distinct('fromUser', 'toUser')
#Reverse query -> messages = Message.objects.order_by('fromUser','toUser','-createdAt').distinct('fromUser', 'toUser')


class ServicePackage(models.Model):
	serviceprovider = models.ForeignKey(ServiceProvider, related_name='service_provider', on_delete=models.CASCADE)
	service = models.ForeignKey(Service, related_name='service_package', on_delete=models.CASCADE)
	name = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	delivery_timeline = models.CharField(max_length=100)
	detail = models.TextField(help_text='separate each on a new line')#separate each on a new line
	cost = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name

	def get_detail_list(self):
		return self.detail.split('\n')


#For posting jobs
class PostProject(models.Model):
	client = models.ForeignKey(User, related_name='client', on_delete=models.CASCADE)
	serviceprovider = models.ForeignKey(ServiceProvider, related_name='project_awardee', default='', null=True, on_delete=models.CASCADE)
	#post_date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=500)
	category = models.ForeignKey(ServiceCategory, blank=True, on_delete=models.CASCADE)
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	#When the project is completed and payment made, then this is turned to True
	completed = models.BooleanField(default=False)
	description = models.TextField()
	image = models.ImageField(blank=True)
	other_information = models.TextField(blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('home:postedproject', args=[self.id])


#Service providers adding sample to their dashboard for display
class SampleServiceDisplay(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	servicecategory = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	search_tags = models.CharField(max_length=500, blank=True)
	description = models.TextField()
	sample_image = models.ImageField(blank=True)

	def __str__(self):
		return self.service.name

	@property
	def service_name(self):
		return self.service.name
	
	@property
	def user_name(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('home:postedsample', args=[self.id, self.slug])

#For placing bids on available projects
class ProjectBid(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	project = models.ForeignKey(PostProject, on_delete=models.CASCADE)
	bidder = models.ForeignKey(ServiceProvider, related_name='bidding_provider', on_delete=models.CASCADE)
	client = models.ForeignKey(User, related_name='project_owner', on_delete=models.CASCADE)
	service = models.ForeignKey(Service, related_name='project_service', on_delete=models.CASCADE)
	#slug = models.SlugField()
	cost = models.DecimalField(max_digits=10, decimal_places=2)
	commission = models.DecimalField(max_digits=10, decimal_places=2)
	bid_reference = models.CharField(max_length=50)
	total_cost = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.project.title 

	def get_absolute_url(self):
		return reverse('home:projectbids', args=[self.project.id])


class ServiceRequest(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	# client = models.ForeignKey(User, on_delete=models.PROTECT),
	vendor = models.ForeignKey(User, related_name="provider", on_delete=models.CASCADE)
	service_user = models.ForeignKey(User, related_name="client_user", on_delete=models.CASCADE) # Due to django's mood-swings, I used this for clients
	delivery = models.BooleanField(default=True)   # This is true cos we will be doing delivery for items
	delivery_duration = models.CharField(max_length=200, null=True, blank=True)  # For vendor to let the client know when the service will be ready 
	cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #Vendor's total charge
	service_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Percentage of vendor's charge
	delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Delivery charge
	total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Vendor's charge + service_fee + delivery
	client_confirmation = models.BooleanField(default=False)   # For client to confirm acceptance of fee 
	payment_made = models.BooleanField(default=False)   #  This will check payment model if payment is made, once made, set to True and send to client to begin production
	service_dispatched = models.BooleanField(default=False)  # For vendor to notify the client when item is en route to e delivered
	delivered = models.BooleanField(default=False)  # For client to confirm delivery, so vendor can be paid  
	vendor_paid = models.BooleanField(default=False)  # Set to True if money is transfered to vendor's servapp-wallet. 

	def __str__(self):
		return self.vendor.username

	@property
	def service_user_name(self):
		return self.service_user.username
	
	@property
	def vendor_name(self):
		return self.vendor.username

	@property
	def service_name(self):
		return self.service.name



class Transaction(models.Model):
	client = models.ForeignKey(User, related_name='service_client', on_delete=models.CASCADE)
	serviceprovider = models.ForeignKey(ServiceProvider, related_name='transaction_serviceprovider', on_delete=models.CASCADE)
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	project = models.ForeignKey(PostProject, on_delete=models.CASCADE)
	selected_bid = models.ForeignKey(ProjectBid, on_delete=models.CASCADE)
	cost = models.DecimalField(max_digits=10, decimal_places=2)
	paid = models.BooleanField(default=False)
	delivered = models.BooleanField(default=False)
	service_returned = models.BooleanField(default=False)
	completed = models.BooleanField(default=False)
	#''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
	#''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
	reference = models.CharField(max_length=50)

	def __str__(self):
		return self.service +':'+self.client.username

	def get_absolute_url(self):
		return reverse('home:transaction', args=[self.id])


#Service provider review by clients
#Review should be sent to service providers by email
class ClientReview(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	serviceprovider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	#Create a transaction model that to have references when client and service provider agrees on a service
	transaction_id = models.CharField(max_length=500)
	review = models.TextField()

	def __str__(self):
		return 'Review for '+ self.service.name

#For accounts
#class MakePayment(models.Model):






































class Dialog(TimeStampedModel):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs", on_delete=models.CASCADE)
	opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"), on_delete=models.CASCADE)

	def __str__(self):
		return self.opponent.username


class Message(TimeStampedModel, SoftDeletableModel):
	dialog = models.ForeignKey(Dialog, related_name='messages', on_delete=models.CASCADE)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages", on_delete=models.CASCADE)
	text = models.TextField(verbose_name=_("Message_text"))
	read = models.BooleanField(verbose_name=_("Read"), default=False)
	all_objects = models.Manager()

	def get_formatted_create_datetime(self):
		return dj_date(localtime(self.created), settings.DATETIME_FORMAT)


	def __str__(self):
		return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"








# Create your models here.
