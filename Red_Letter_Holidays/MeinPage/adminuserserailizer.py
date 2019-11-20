from rest_framework import serializers
from .models import *

class BookingSerailizer(serializers.ModelSerializer):
	class Meta:
		model=Booking
		fields='__all__'

