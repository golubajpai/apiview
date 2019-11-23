from .models import *
from .views import *
from .serializer import *
from .adminuserserailizer import *
from .authantication import *


class UserBooking(viewsets.ModelViewSet):
	permission_classes=( Token_auth,)
	
	queryset=Booking.objects.all()
	serializer_class=BookingSerailizer

	
	def get_queryset(self):
		x=Token.objects.get(key=self.request.data['token']).user
		if x.is_superuser:
			return Booking.objects.all()
		else:
			return Booking.objects.filter(user=x)


	def perform_create(self,serializer):
		
		serializer.save(user=Token.objects.get(key=self.request.data['token']).user)



class UpdateUserPackage(viewsets.ModelViewSet):
	permission_classes=(Token_auth,)
	serializer_class=UpdateUserHotelSerializer
	

	def get_queryset(self):
		user=Token.objects.get(key=self.request.data['token']).user
		if user.is_superuser:
			return AvailabilityoFhotel.objects.all()
		else:
			x=Booking.objects.get(user=user)
			return AvailabilityoFhotel.objects.filter(booking=x)


'''class UpdateDataUserview(viewsets.ModelViewSet):
	permission_classes=( Token_auth,)
	serializer_class=UpdateDataUserviewserailizer
'''

class Updateddata(viewsets.ModelViewSet):
	serializer_class=PackageSerelizer
	def get_queryset(self):
		#import pdb;pdb.set_trace()
		queryset=Package.objects.filter(updated=True,user=Token.objects.get(key=self.request.data['token']).user)
		return queryset
