from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
#


# Create your views here.
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from .serializer import *
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login ,logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core import exceptions 
import random
import os
from rest_framework import generics
import os
from sendgrid import SendGridAPIClient
from braces.views import CsrfExemptMixin
from rest_framework import viewsets
import json


from sendgrid.helpers.mail import Mail







           
class Data(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self,request):
		data=User.objects.all()
		name= UserObjects(data, many=True)
		return Response(name.data)

class UserCreateAPIView(CsrfExemptMixin,generics.CreateAPIView):
	serializer_class = UserSerializer

	def create(self, request, *args, **kwargs):
		
		serializer=self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		
		token, created = Token.objects.get_or_create(user=serializer.instance)
		return Response({'token': token.key,'message':"User Created successfully"
}, status=status.HTTP_201_CREATED,headers={"Access-Control-Allow-Origin":"*"})
		

class Logout(APIView):
    permission_classes = (TokenAuthentication,)
    
    def get(self, request, format=None):
        import pdb;pdb.set_trace()
        # simply delete the token to force a login
        logout(request.user)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

	


class LoginData(APIView):
	



	def post(self,request):

		serelize=UserLogin(data=request.data)
		#import pdb; pdb.set_trace()
		serelize.is_valid(raise_exception=True)
		objectuser=serelize.validated_data
		#import pdb;pdb.set_trace()
		login(request,objectuser)
		token, _ = Token.objects.get_or_create(user=objectuser)
		return Response({'token':token.key,},status=status.HTTP_200_OK,headers={"Access-Control-Allow-Origin":"*"})

class Reset_Password(CsrfExemptMixin,APIView):
	

	def post(self,request):
		x=random.randint(100000,999999)
		serelize=Reset(data=request.data)

		serelize.is_valid(raise_exception=True)
		print(serelize.validated_data)
		#import pdb;pdb.set_trace()
		print('ok')
		
		user_data=serelize.validated_data['user']
		#import pdb;pdb.set_trace()

		serelize.save(user=user_data,reset_token=str(x))
		
		message = Mail(
		from_email='priyambajpai.liseinfotech@gmail.com',
		to_emails=user_data.email,
		subject='Reset Password',
		html_content='<strong>your password opt is {}</strong>'.format(x))
		msg='reset password otp has been sent to this mail - {}'.format(user_data.email)
		try:
			sg = SendGridAPIClient('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')
			sg.send(message)
			return Response({"message sent":msg},status=status.HTTP_200_OK)

		except Exception as e:
			return Response({"message sent":'can not reset password right now'},status=404,headers={"Access-Control-Allow-Origin":"*"})
		
	

class Valid_token(APIView):
	def post(self,request):
		x=Reset_token(data=request.GET)
		x.is_valid(raise_exception=True)
		validated=x.validated_data['user']
		user_instance=validated.user
		model=user_instance.set_password(x.validated_data['password'])
		model.save()


		return Response({'password':'password has been changed successfully'},headers={"Access-Control-Allow-Origin":"*"})


class HotelView(viewsets.ModelViewSet):
	#queryset=Hotel.objects.all()
	serializer_class=HotelSerelizer

	def perfome_create(self,serializer):
		obj=serializer.save()
		for x in self.request.data.getlist('image'):
			mf=MyFile.obj.create(image=x)
			obj.image.add(mf)
	def get_queryset(self):
		a=[]
		
		try:
			y=self.request.GET['hotel']
			##import pdb;pdb.set_trace()

			if y:
				data  = json.loads(y)
				
				for x in data:
					print(x)
					

					query=Hotel.objects.filter(city=x)
					a.append(query)
				return a
		except:
			query=Hotel.objects.all()
			return query

	




	

class PackageView(viewsets.ModelViewSet):
	
	serializer_class=PackageSerelizer

	def get_queryset(self):
	 	query=Package.objects.all()
	 	return query



		


  
class Get_hot_deals(viewsets.ModelViewSet):
	serializer_class=PackageSerelizer

	def get_queryset(self,*args,**kwargs):
		query=Package.objects.filter(hot_deal_package=True)
		return query

class Google_Facebook_login(APIView):
	def post(self,request):
		x=GoogleSerelizer(data=request.data)
		#import pdb ;pdb.set_trace() 
		x.is_valid(raise_exception=True)
		#import pdb ;pdb.set_trace()
		
		if 'user' in x.validated_data:
			k=x.validated_data['token']
			objectuser=x.validated_data['user']
			n=UserSerializer(x.validated_data['objects'])
			#token=Token.objects.get(user=x.validated_data['objects'])
			#token.key=k
			#token.save()
			Token.objects.filter(user=x.validated_data['objects']).update(key=k)

			
			
			return Response({'token':k,'message':'user logged in successfully','user':n.data}, status=status.HTTP_201_CREATED,headers={"Access-Control-Allow-Origin":"*"})
		else:
			y=SocialSerializer(data=request.data)

			y.is_valid(raise_exception=True)
			y.save()
			#import pdb ;pdb.set_trace()
			
			return Response({'token':y.validated_data['token'],'message':"User Created successfully"
}, status=status.HTTP_201_CREATED,headers={"Access-Control-Allow-Origin":"*"})

			





	





