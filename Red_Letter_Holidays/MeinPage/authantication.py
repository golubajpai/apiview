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
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000






class IsAdminOrReadOnly(BasePermission):
    """

    The request is authenticated as a user, or is a read-only request.
    """
    SAFE_METHODS = ['GET']

    def has_permission(self, request, view):
        #import pdb;pdb.set_trace()
        
        try:
            data=request.data['token']
            superuser=Token.objects.get(key=data)
            print(superuser.user)
            superuser=Token.objects.get(key=data)
            y=User.objects.get(email=superuser.user)
            
            if (request.method in self.SAFE_METHODS or (y.is_staff==True)):
                    return True
            else:
                False
        
        except:
            return False
            raise exceptions.validationError('Only admin can access these method')