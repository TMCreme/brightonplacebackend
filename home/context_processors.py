from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import ServiceCategory, Service, ServiceProvider, SampleServiceDisplay
from .forms import UserLogin

def baseview(request):
	catt = ServiceCategory.objects.all()
	servcc = Service.objects.all()
	servsam = SampleServiceDisplay.objects.all()
	user_login_form = UserLogin
		
	return {'catt':catt, 'servcc':servcc, 'servsam':servsam}





