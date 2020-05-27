from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import (
	ServiceCategory, Service, ServiceProvider, ServicePackage, SampleServiceDisplay,
	Message, MessageInbox, UserLocation, UserProfile
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = '__all__'
		extra_kwargs = {'id': {'read_only': False}}


	def create(self, validated_data):
		user = super(UserSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.is_active = True
		user.save()
		return user


class UserProfileSerializer(serializers.ModelSerializer):
	id = serializers.ReadOnlyField()
	username = serializers.CharField(source='user.username', read_only=True)
	email = serializers.EmailField(source='user.email', read_only=True)

	class Meta:
		model = UserProfile
		fields = '__all__'



class ServiceCategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    
    class Meta:
        model = ServiceCategory
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': False}}

class ServiceProviderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    
    class Meta:
        model = ServiceProvider
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': False}}


class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': False}}




class UserLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserLocation
		fields = ['region','district','locality','latitude','longitude','']
		extra_kwargs = {'id': {'read_only': False}}




class SampleServiceDisplaySerializer(serializers.ModelSerializer):
	service_name = serializers.ReadOnlyField()
	user_name = serializers.ReadOnlyField()
	id = serializers.ReadOnlyField()
	class Meta:
		model = SampleServiceDisplay
		fields = '__all__'
		extra_kwargs = {'id': {'read_only': False}}





