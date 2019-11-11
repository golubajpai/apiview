from rest_framework import serializers
from .models import User ,Token_data
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.core import exceptions 
import random

User = get_user_model()
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

	def create(self, validated_data):
		return Token_data.objects.create(**validated_data)

class Reset_token(serializers.ModelSerializer):
	class Meta:
		model=Token_data
		fields='__all__'


		

		





