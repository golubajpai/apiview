from django.contrib import admin
from django.urls import path, include
from .views import *
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
	'delete':'destroy'

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
hotel_city_get=HotelCityView.as_view({
	'get':'list',
	'post':'create',

	})
hotel_city=HotelCityView.as_view({
	'get':'retrieve',
	'put':'update',
	'patch':'partial_update',
	'delete':'destroy'

	})


urlpatterns = [
    
	path('',Data.as_view(),name='index'),
	path('register/',UserCreateAPIView.as_view(),name='user'),
	path('login/',LoginData.as_view(),name='login'),
	path('logout/',Logout.as_view(),name='logout'),
	path('passwordreset/',Reset_Password.as_view(),name='resetpassword'),
	path('passwordconfirm/',Valid_token.as_view(),name='passwordconfirm'),
	path('viewhotel/',hotel_list,name='viewhotel'),
	path('packages/',package_list,name='packages'),
	path('packages/<int:pk>/',packages_data,name='packages'),
	path('viewhotel/<int:pk>/',hotel_data,name='viewhotel'),

	path('sociallogin/',Google_Facebook_login.as_view(),name='sociallogin'),
	path('getHotDeals/',get_hot_deals,name='Gethotdeals'),
	path('hotelimagespacific/<int:pk>/',Hotel_image_spacific,name='gethotelimagespacific'),
	path('gethotelimage/',Hotel_image,name='Gethotelimage'),
	path('gethotelimage/<int:pk>/',Hotel_image_spacific,name='Gethotelimage'),
	path('gethotelcity/<int:pk>/',hotel_city,name='Gethotelimage'),
	path('gethotelcity/',hotel_city_get,name='Gethotelimage')

]
