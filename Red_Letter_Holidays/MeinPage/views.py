from .authantication import *

 







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
    permission_classes = (IsAuthenticated,)  
    
    def get(self, request, format=None):
        #import pdb;pdb.set_trace()
        # simply delete the token to force a login
        
        request.user.auth_token.delete()
        
        return Response(status=status.HTTP_200_OK)

	


class LoginData(APIView):
	



	def post(self,request):

		serelize=UserLogin(data=request.data)
		#import pdb; pdb.set_trace()
		serelize.is_valid(raise_exception=True)
		objectuser=serelize.validated_data
		
		
		#import pdb;pdb.set_trace()
		token, _ = Token.objects.get_or_create(user=objectuser)
		return Response({'token':token.key,'message':'User login successfully'},status=status.HTTP_200_OK,headers={"Access-Control-Allow-Origin":"*"})

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


		return Response({'message':'password has been changed successfully'},status=status.HTTP_200_OK,headers={"Access-Control-Allow-Origin":"*"})


class HotelView(viewsets.ModelViewSet):
	
	permission_classes = (IsAdminOrReadOnly,)
	queryset=Hotel.objects.all()
	def get_serializer_class(self):
		x=['create','update','partial_update','destroy']
		if self.action in x:
			return HotelSerelizerCreate
		else:
			return HotelSerelizer

class HotelCityView(viewsets.ModelViewSet):
	permission_classes=(IsAuthenticated,)
	queryset=Hotel_cities.objects.all()
	def get_serializer_class(self):
		return HotelCitySeailizer



	



class Hotel_Image(viewsets.ModelViewSet):
	permission_classes = (IsAdminOrReadOnly,)
	serializer_class=HotelImages
	queryset=HotelImage.objects.all()
	

class PackageView(viewsets.ModelViewSet):
	permission_classes = (IsAdminOrReadOnly,)
	
	serializer_class=PackageSerelizer
	pagination_class = LargeResultsSetPagination
	paginate_by = 20


	def get_queryset(self):
		
		if 'search' in self.request.GET:
			a=self.request.GET['search']
			import pdb;pdb.set_trace()
			queryset = Package.objects.filter(package_city__package_city__contains=a) | Package.objects.filter(Country__contains=a) | Package.objects.filter(Package_name__contains=a)
			#import pdb;pdb.set_trace()
			print(queryset)
			return queryset
		else:
			return Package.objects.all()




  
class Get_hot_deals(viewsets.ModelViewSet):
	permission_classes = (IsAdminOrReadOnly,)
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

			





	





