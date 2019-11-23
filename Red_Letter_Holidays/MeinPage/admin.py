from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Hotel)

admin.site.register(Package)
admin.site.register(PackageImage)
admin.site.register(HotelImage)
admin.site.register(Package_city)
admin.site.register(Package_schedule)
admin.site.register(Exclusions)
admin.site.register(Booking)
admin.site.register(Transfer_sic)

