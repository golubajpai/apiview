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
from rest_framework import pagination
from rest_framework.permissions import BasePermission 

from sendgrid.helpers.mail import Mail


users = User.objects.all()
for user in users:
    token, created = Token.objects.get_or_create(user=user)




class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000






class IsAdminOrReadOnly(BasePermission):

    SAFE_METHODS = ['GET']

    def has_permission(self, request, view):
        
        if request.method=='GET':
            return True

        
        try:
            if type(request.data)==list:
                data=request.data[0]['token']

            else:
                data=request.data['token']
                #import pdb;pdb.set_trace()

            
            
            #import pdb;pdb.set_trace()
            y=Token.objects.get(key=data).user

                
            
            if (request.method=='GET' or (y.is_staff==True)):
                    return True
            else:
                False
        
        except:

            return False
class Only_Admin:
    def has_permission(self,request,data):
        try:
            if request.data['token']:
                    User=Token.objects.get(key=request.data['token']).user
                    
                    if User.is_staff and User.is_superuser:

                        return True
                    else:
                        return False

            else:
                return False
        except:
            return False


class Token_auth:
    SAFE_METHODS = ['GET','POST',]
    ADMIN_METHODS=['GET','POST','PUT','PATCH','DELETE']
    def has_permission(self,request,data):
        if request.method :
            try:
                if request.data['token']:
                    User=Token.objects.get(key=request.data['token']).user
                    
                    if User.is_staff and User.is_superuser and request.method in self.ADMIN_METHODS :

                        return True
                    if User and request.method in self.SAFE_METHODS:
                        return True

                    
            except:
                
                return False
        return False


