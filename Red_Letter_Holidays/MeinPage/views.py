from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
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
from sendgrid.helpers.mail import Mail







           
class Data(APIView):
	permission_classes = (TokenAuthentication,)  
	def get(self,request):
		data=User.objects.all()
		name= UserObjects(data, many=True)
		return Response(name.data)

class UserCreateAPIView(generics.CreateAPIView):
	serializer_class = UserSerializer

	def create(self, request, *args, **kwargs):
		
		serializer=self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		
		token, created = Token.objects.get_or_create(user=serializer.instance)
		return Response({'token': token.key,'message':"User logged in successfully"
}, status=status.HTTP_201_CREATED)
		

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
		return Response({'token':token.key,},status=status.HTTP_200_OK)

class Reset_Password(APIView):
	

	def post(self,request):
		x=random.randint(100000,999999)
		serelize=Reset(data=request.data)

		serelize.is_valid(raise_exception=True)
		print(serelize.validated_data)
		#import pdb;pdb.set_trace()
		
		user_data=User.objects.get(email=serelize.validated_data['email'])
		serelize.save(user=user_data,reset_token=x)
		
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
			return Response({"message sent":'can not reset password right now'},status=404)
		
	

#class Valid_token(APIView):
#	def patch(self,request):
#		x=Reset_token(valid=True)
#		x.is_valid(raise_exception=True)
#		x.save()
#		return Response({'token':'Token is valid'})





