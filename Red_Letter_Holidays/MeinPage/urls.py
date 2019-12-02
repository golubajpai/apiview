from django.contrib import admin
from django.urls import path, include
from .views import *
from .adminuser import *
from rest_framework.routers import DefaultRouter,SimpleRouter
router=DefaultRouter()
router.register('hotel',HotelView,base_name='Hotel')
hotel_list=HotelView.as_view({
	'get':'list',
	'post':'create',

	})
hotel_data=HotelView.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy',


	})
package_list=PackageView.as_view({
	'get':'list',
	'post':'create'
	})
packages_data=PackageView.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})

get_hot_deals=Get_hot_deals.as_view({
	'get':'list'
	})
Hotel_image=Hotel_Image.as_view({
	'get':'list',
	'post':'create'
	})
Hotel_image_spacific=Hotel_Image.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	


	})
exclusion=Exclusion.as_view({
	'post':'create',
	'get':'list'
	})

package_schedule=Package_Schedule.as_view({
	'post':'create',
	'get':'list'
	})
package_schedule_spacific=Package_Schedule.as_view({
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})
booking=UserBooking.as_view({
	'get':'list',
	'post':'create'
	})
bookingupdate=UserBooking.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})
UpdateUserPackageurl=UpdateUserPackage.as_view({
	'post':'create',
	'get':'list'
	})
updateddata=Updateddata.as_view({
	'get':'list'
	})

transfer_sic=Transfet.as_view({
	'get':'list',
	'post':'create'
	})

transfer_sic_spacific=Transfet.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
	})
flight_inbond=Flight_inbond.as_view({
	'get':'list',
	'post':'create'
	})
flight_inbond_retrive=Flight_inbond.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'
})
flight_outbond=Flight_outbond.as_view({
	'get':'list',
	'post':'create'

	})
flight_outbond_retraive=Flight_outbond.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'

	})
pakageimage1=PackageImageView.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'

	})
pakageimage2=PackageImageView.as_view({
	'get':'list',
	'post':'create'

	})

urlpatterns = [
    
	path('',Data.as_view(),name='index'),
	path('getuser/',GetUser.as_view()),
	path('flight_outbond/<int:pk>/',flight_outbond_retraive),
	path('flight_outbond/',flight_outbond),
	path('flight_inbond/<int:pk>/',flight_inbond_retrive),
	path('flight_inbond/',flight_inbond),
	path('transfer/',transfer_sic),
	path('transfer/<int:pk>/',transfer_sic_spacific),
	path('booking/',booking,name='booking'),
	path('booking/<int:pk>/',bookingupdate,name='bookingupdate'),
	path('updateddata/',updateddata),
	path('packageschedule/<int:pk>/',package_schedule_spacific,name='packageschedulespacific'),
	path('packageschedule/',package_schedule,name='packageschedule'),
	path('register/',UserCreateAPIView.as_view(),name='user'),
	path('login/',LoginData.as_view(),name='login'),
	path('logout/',Logout.as_view(),name='logout'),
	path('restpassword/',Reset_Password.as_view(),name='resetpassword'),
	path('passwordconfirm/',Valid_token.as_view(),name='passwordconfirm'),
	path('viewhotel/',hotel_list,name='viewhotel'),
	path('packages/',package_list,name='packages'),
	path('packages/<int:pk>/',packages_data,name='packages'),
	path('viewhotel/<int:pk>/',hotel_data,name='viewhotel'),
	path('adminlogin/',AdminLoginData.as_view(),name='adminlogin'),
	path('verify_token/',Verify_token.as_view(),name='verify_token'),
	path('packageimage/',pakageimage2),
	path('packageimage/<int:pk>',pakageimage1),

	path('sociallogin/',Google_Facebook_login.as_view(),name='sociallogin'),
	path('getHotDeals/',get_hot_deals,name='Gethotdeals'),
	path('hotelimagespacific/<int:pk>/',Hotel_image_spacific,name='gethotelimagespacific'),
	path('gethotelimage/',Hotel_image,name='Gethotelimage'),
	path('gethotelimage/<int:pk>/',Hotel_image_spacific,name='Gethotelimage'),
	path('exclusion/',exclusion,name='Gethotelimage'),
	path('updateuserhoteladmin/',UpdateUserPackageurl)

]
