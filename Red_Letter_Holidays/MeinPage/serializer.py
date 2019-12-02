from rest_framework import serializers
from .models import User ,Token_data
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.core import exceptions 
import random
from rest_framework.urlpatterns import format_suffix_patterns

from .models import *
from rest_framework import serializers, fields



User = get_user_model()

class Varify_token_serelizers(serializers.Serializer):
	password_token=serializers.CharField(max_length=200)
	def validate(self,data):
		token=data.get('password_token')
		try:
			data=Token_data.objects.get(reset_token=token)
			x={'token':token}
			return x
		except:
			raise  exceptions.ValidationError('invalid password token')

class exclusion_serailizers(serializers.ModelSerializer):
	class Meta:
		model=Exclusions
		fields='__all__'
class Package_schedule_serailizers (serializers.ModelSerializer):
	class Meta:
		model=Package_schedule
		fields='__all__'
class Create_package_serailizers(serializers.ModelSerializer):
	class Meta:
		model=Package
		fields='__all__'

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
    	fields="__all__"
class HotelSerelizerCreate(serializers.ModelSerializer):
	class Meta:
		model=Hotel
		fields='__all__'



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




class AdminLogin(serializers.ModelSerializer):
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
			try:
				if auth.is_superuser and auth.is_staff:
					return auth
			except:
					raise  exceptions.ValidationError('credentials invalid')
		else:
			raise exceptions.ValidationError('fill all the fields')


class Reset(serializers.ModelSerializer):

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

class Reset_token(serializers.Serializer):
	token=serializers.CharField(max_length=200)
	password=serializers.CharField(max_length=200)
	

	def validate(self,data):
		#import pdb;pdb.set_trace()
		token=data.get('token')
		password=data.get('password')
		if token and password:
			try:
				x=Token_data.objects.get(reset_token=token)
				user={'user':x.user,'new_password':password,'otp':x}
				
				return user
			except:
				raise exceptions.ValidationError('invalid otp')
		else:
			raise exceptions.ValidationError('fill all the fields')
class HotelImages(serializers.ModelSerializer):
	class Meta:
		model=HotelImage
		fields='__all__'


class HotelImageSerializer(serializers.ModelSerializer):
	image_id=serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.filter(updated=False),source='image_hotel.id')
	class Meta:
		model=HotelImage
		fields=('image_data','image_id',)

class PackageImageSere(serializers.ModelSerializer):
	image_id=serializers.PrimaryKeyRelatedField(queryset=Package.objects.filter(updated=False),source='image_package.id')
	class Meta:
		model=PackageImage
		fields=('image_data','image_id',)


class HotelSerelizer(serializers.ModelSerializer):
	hotel=serializers.PrimaryKeyRelatedField(queryset=Package.objects.filter(updated=False),source='id')
	image_hotel=HotelImageSerializer(many=True)
	
	class Meta:
		model=Hotel
		fields=('hotel','rating','hotel_name','hotel_city','hotel_address','room_type','inclusive','meal_type','amenities','price','image_hotel','available')		

class Package_city(serializers.ModelSerializer):
	
	class Meta:
		model=Package_city
		fields='__all__'

class Flight_inbound_serailizer(serializers.ModelSerializer):
	class Meta:
		model=Flight_inbound
		fields='__all__'
class Flight_outbond_serailizer(serializers.ModelSerializer):
	class Meta:
		model=Flight_outbound
		fields='__all__'
class Transfer_sic_serelizer(serializers.ModelSerializer):
	class Meta:
		model=Transfer_sic
		fields="__all__"
class Transfer_private_serailizer(serializers.ModelSerializer):
	class Meta:
		model=Transfer_private
		fields='__all__'
class PackageSerelizer(serializers.ModelSerializer):

	hotel=HotelSerelizer(many=True)
	Start_date=fields.DateField(input_formats=["%Y-%m-%d"])
	End_date=fields.DateField(input_formats=["%Y-%m-%d"])
	Flight_inbound_data=Flight_inbound_serailizer(many=True)
	package_schedule =Package_schedule_serailizers(many=True)
	Flight_outbound_data=Flight_outbond_serailizer(many=True)
	packageImage=PackageImageSere(many=True)

	package_city=Package_city(many=True)
	
	exclusions=exclusion_serailizers(many=True)
	transfer_sic=Transfer_sic_serelizer(many=True)
	Transfer_private=Transfer_private_serailizer(many=True)

	class Meta:
		model=Package
		fields=('id','Package_name','packageImage','Package_discription','Transfer_private','transfer_sic','Flight_inbound_data','Flight_outbound_data','exclusions','package_schedule','package_city','Country','Totel_price','Meal_included','Itnerary','Company_details'
			,'Transfer_private','Freebies','image_package'
			,'Start_date','End_date','Flight_prise','Land_price','hotel')
			


		
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


		





