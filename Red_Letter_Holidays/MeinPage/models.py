from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('termsAccepted',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    """User model."""

    username = None
    first_name=None
    last_name=None
    name=models.CharField(max_length=30,blank=True)
    email = models.EmailField(_('email address'), unique=True)
    city=models.CharField(max_length=30, blank=True)
    profile_pic=models.ImageField(blank=True)
    phone=models.CharField(max_length=10)
    termsAccepted=models.BooleanField()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Token_data(models.Model):
    email=models.CharField(max_length=100)
    reset_token=models.CharField(max_length=6)
    time=models.TimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE , related_name="books")



    def __str__(self):
        return '%s: %s' % (self.Cities, self.Country)



class Hotel(models.Model):
    hotel_name=models.CharField(max_length=255)
    hotel_city=models.CharField(max_length=255)
    rating=models.CharField(max_length=255)
    hotel_address=models.CharField(max_length=255)
    room_type=models.CharField(max_length=255)
    inclusive=models.CharField(max_length=255)
    meal_type=models.CharField(max_length=255)
    amenities=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    user=models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    updated=models.BooleanField(default=False)
    available=models.BooleanField(default=True)

    
    

    def __str__(self):
        return '%s: %s' % (self.hotel_name, self.hotel_address)

    
class Transfer_sic(models.Model):
    transfer_sic_data=models.CharField(max_length=255)
    available=models.BooleanField(default=True)
class Transfer_private(models.Model):
    transfer_private_data=models.CharField(max_length=255)
    available=models.BooleanField(default=True )
class Flight_inbound(models.Model):
    flight_inbound=models.CharField(max_length=255)
    available=models.BooleanField(default=True)

class Flight_outbound(models.Model):
    flight_outbound=models.CharField(max_length=255)
    available=models.BooleanField(default=True)
class Package(models.Model):
    Package_name=models.CharField(max_length=255)
    Package_discription=models.TextField()
    Country=models.CharField(max_length=255)
    Start_date=models.CharField(max_length=200)
    End_date=models.CharField(max_length=255)
    Flight_inbound_data=models.ManyToManyField(Flight_inbound,related_name='flight_inbound_data')
    Flight_outbound_data=models.ManyToManyField(Flight_outbound,related_name='Flight_outbound_data')
    Flight_prise=models.CharField(max_length=255)
    Land_price=models.CharField(max_length=255)
    Totel_price=models.CharField(max_length=255)
    Meal_included=models.CharField(max_length=255)
    transfer_sic=models.ManyToManyField(Transfer_sic,related_name='transfer_sic_of_package')
    Visa_included=models.CharField(max_length=255)
    
    
    Meal_included=models.CharField(max_length=255)
    Itnerary=models.TextField()
    Company_details=models.CharField(max_length=255)
    Transfer_private=models.ManyToManyField(Transfer_private,related_name='transfer_private')
    Freebies=models.CharField(max_length=255)
    Transfer_detail_seperate=models.CharField(max_length=255)
    Transfesic=models.CharField(max_length=255)
    discount=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    duration=models.CharField(max_length=255)
    hotel=models.ManyToManyField(Hotel,related_name='hotel')
    hot_deal_package=models.BooleanField()
    user=models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    updated=models.BooleanField(default=False)
    
   
    

    def __str__(self):
        return (self.Package_name)


class Activities(models.Model):
    package_id=models.ForeignKey(User,related_name='package_id',on_delete=models.CASCADE)
    activities=models.CharField(max_length=255)


class Booking(models.Model):
    user=models.ForeignKey(User,related_name='userbooking',on_delete=models.CASCADE)
    package=models.ForeignKey(Package,related_name='packageforuser',on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default='review')
    completed=models.BooleanField(default=False)
    

class Exclusions(models.Model):
    exclusion_package=models.ForeignKey(Package,related_name='exclusions',on_delete=models.CASCADE)
    excelusion_data=models.CharField(max_length=200)
class Package_schedule(models.Model):
    days=models.CharField(max_length=255)
    discription=models.CharField(max_length=255)
    package=models.ForeignKey(Package,related_name='package_schedule',on_delete=models.CASCADE)
class Package_city(models.Model):
    package_city_id=models.ForeignKey(Package,related_name='package_city',on_delete=models.CASCADE)
    Package_city_image=models.ImageField()
    package_city=models.CharField(max_length=50)


class HotelImage(models.Model):
    image_hotel=models.ForeignKey(Hotel,related_name='image_hotel',on_delete=models.CASCADE)
    image_data=models.ImageField()
class PackageImage(models.Model):
    image_package=models.ForeignKey(Package,related_name='image_package',on_delete=models.CASCADE)
    image_data=models.ImageField()


class AvailabilityoFhotel(models.Model):
    booking=models.ForeignKey(Booking,related_name='booking', on_delete=models.CASCADE)
    hotel_id=models.ForeignKey(Hotel,related_name='availhotel',on_delete=models.CASCADE)
    hotel_availeble=models.BooleanField(default=True)
    hotel_price=models.CharField(max_length=20,default='No Changes')

class PriseOfPackage(models.Model):
    booking=models.ForeignKey(Booking,related_name='bookingprise',on_delete=models.CASCADE)
    totel_price=models.CharField(max_length=20,default='No Changes')








