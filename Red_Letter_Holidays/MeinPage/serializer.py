from rest_framework import serializers
from .models import User ,Token_data
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.core import exceptions 
import random
from .models import *

User = get_user_model()
class SocialSerializer(serializers.ModelSerializer):
    token=serializers.CharField(write_only=True)
    

    class Meta:
        model = User
        fields = '__all__'
    def validate(self,data):

    	token=data.get('token')
    	#import pdb;pdb.set_trace()
    	x=data.pop('token')
    	if not x:
    		raise exceptions.ValidationError('token not found')
    	else:
    		return {'data':data,'token':x}

    def create(self,validated_data):
    	User=super(SocialSerializer,self).create(validated_data['data'])
    	User.set_unusable_password()
    	User.save()

    	#import pdb;pdb.set_trace()
    	token = Token.objects.create(user=User,key=validated_data['token'])
    	
    	return (User,token)
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self,validated_data):
    	User=super(UserSerializer,self).create(validated_data)
    	User.set_password(validated_data['password'])
    	User.save()
    	
    	return User

class UserObjects(serializers.ModelSerializer):
    class Meta:
    	model=User
    	fields=('first_name','last_name','email','password')



class UserLogin(serializers.ModelSerializer):
	email=serializers.CharField(max_length=50)
	password=serializers.CharField(max_length=20)
	class Meta:
		model = User
		fields = ('email','password')


	def validate(self,data):
		email=data.get('email')
		password=data.get('password')
		#import pdb ;pdb.set_trace()
		if email and password:
			auth=authenticate(email=email,password=password)
			if auth:
				return auth
			else:
				raise  exceptions.ValidationError('credentials invalid')
		else:
			raise exceptions.ValidationError('fill all the fields')



class Reset(serializers.ModelSerializer):
	#reset_token=serializers.CharField(max_length=20)
	#ip_add=serializers.CharField(max_length=40)
	

	class Meta:
		model=Token_data
		fields=('email',)
	def validate(self,data):
		email_get=data.get('email')

		if email_get:
			try:
				x=User.objects.get(email=email_get)
				y={'user':x}
				return y
			except:
				raise exceptions.ValidationError('Invalid e-mial address')
		else:
			raise exceptions.ValidationError('Please fill the email field')

	def create(self, validated_data):
		return Token_data.objects.create(**validated_data)

class Reset_token(serializers.ModelSerializer):
	class Meta:
		model=Token_data
		fields='__all__'

	def validate(self,data):
		token=data.get('token')
		password=data.get('password')
		if token and password:
			try:
				x=Token_data.objects.get(reset_token=token)
				user={'user':x.user,'new_password':password}
				return user
			except:
				raise exceptions.ValidationError('invalid otp')
		else:
			raise exceptions.ValidationError('fill all the fields')

class HotelSerelizer(serializers.ModelSerializer):
	class Meta:
		model=Hotel
		fields='__all__'

class PackageSerelizer(serializers.ModelSerializer):
	class Meta:
		model=Package
		fields='__all__'



		
class GoogleSerelizer(serializers.Serializer):
	token=serializers.CharField(write_only=True)
	email=serializers.CharField(write_only=True)
	class Meta:
		model=User
		filds='__all__'

	def validate(self,data):
		email=data.get('email')
		#import pdb;pdb.set_trace()
		token=data.get('token')
		if email and token:
			try:
				user=User.objects.filter(email=email).exists()
				objects=User.objects.get(email=email)
				x={'user':user,'token':token,'objects':objects}
				return x
			except:
				
				
				return {'data':data}
		else:
			raise exceptions.ValidationError('token not found')


		





