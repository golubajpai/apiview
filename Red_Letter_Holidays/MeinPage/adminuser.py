from .models import *
from .views import *
from .serializer import *
from .adminuserserailizer import *
from .authantication import *


class UserBooking(viewsets.ModelViewSet):
	permission_classes=( Token_auth,)
	serializer_class=BookingSerailizer
	queryset=Exclusions.objects.all()