from rest_framework import serializers
from .models import *
from .serializer import *
class BookingSerailizer(serializers.ModelSerializer):
	class Meta:
		model=Booking
		fields=('package','id','status','completed')
class BookingSerailizerGet(serializers.ModelSerializer):
	package=PackageSerelizer()
	class Meta:
		model=Booking

		fields=('id','status','completed','package',)

class UpdateUserHotelSerializer(serializers.ModelSerializer):
	class Meta:
		model=AvailabilityoFhotel
		fields='__all__'

'''class UpdatedData(serializers.ModelSerializer):
	class Meta:
		model=
'''



	


