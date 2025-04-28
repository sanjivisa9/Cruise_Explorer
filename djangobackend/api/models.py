from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='api_user_set',
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='api_user_set',
        help_text=('Specific permissions for this user.'),
    )
    
    def __str__(self):
        return self.email


class Student(models.Model):
    stuname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Cruise(models.Model):
    type = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    visiting = models.CharField(max_length=1000)
    nights = models.IntegerField(default=0)
    decks = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    startDate = models.DateField()
    endDate = models.DateField()
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cruise/images", default="")

    def __str__(self):
        return self.origin


class CruiseDetail(models.Model):
    type = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    visiting = models.CharField(max_length=1000)
    nights = models.IntegerField(default=0)
    decks = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    startDate = models.DateField()
    endDate = models.DateField()
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cruise/images", default="")
    cruiseName = models.CharField(max_length=100, default="Unnamed Cruise")

    def __str__(self):
        return self.origin


class CruiseDetailFinal(models.Model):
    ROOM_TYPES = [
        ('Oceanview', 'Oceanview'),
        ('Interior', 'Interior')
    ]
    LOCATIONS = [
        ('forward', 'Forward'),
        ('middle', 'Middle'),
        ('aft', 'Aft')
    ]

    type = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    visiting = models.CharField(max_length=1000)
    nights = models.IntegerField(validators=[MinValueValidator(1)])
    decks = models.IntegerField(validators=[MinValueValidator(1)])
    cost = models.IntegerField(validators=[MinValueValidator(0)])
    seats = models.IntegerField(validators=[MinValueValidator(0)])
    startDate = models.DateField()
    endDate = models.DateField()
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    image = models.ImageField(upload_to="cruise/images", default="")
    cruiseName = models.CharField(max_length=100)
    
    # Room counts with validation
    oceanviewRooms = models.IntegerField(validators=[MinValueValidator(0)])
    InteriorRooms = models.IntegerField(validators=[MinValueValidator(0)])
    
    # Location specific room counts
    oceanviewForward = models.IntegerField(validators=[MinValueValidator(0)])
    oceanviewMiddle = models.IntegerField(validators=[MinValueValidator(0)])
    oceanviewAft = models.IntegerField(validators=[MinValueValidator(0)])
    InteriorForward = models.IntegerField(validators=[MinValueValidator(0)])
    InteriorMiddle = models.IntegerField(validators=[MinValueValidator(0)])
    InteriorAft = models.IntegerField(validators=[MinValueValidator(0)])
    
    # Cost fields
    oceanviewRoomsCost = models.IntegerField(validators=[MinValueValidator(0)])
    InteriorRoomsCost = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        indexes = [
            models.Index(fields=['type', 'origin', 'startDate']),
            models.Index(fields=['cruiseName']),
        ]

    def clean(self):
        if self.endDate <= self.startDate:
            raise ValidationError('End date must be after start date')
        
        # Validate total room counts match location-specific counts
        oceanview_total = self.oceanviewForward + self.oceanviewMiddle + self.oceanviewAft
        interior_total = self.InteriorForward + self.InteriorMiddle + self.InteriorAft
        
        if oceanview_total != self.oceanviewRooms:
            raise ValidationError('Oceanview room counts do not match location totals')
        if interior_total != self.InteriorRooms:
            raise ValidationError('Interior room counts do not match location totals')

    def __str__(self):
        return self.cruiseName


class Booking(models.Model):
    cruise = models.ForeignKey(CruiseDetailFinal, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100, choices=CruiseDetailFinal.ROOM_TYPES)
    room_number = models.CharField(max_length=10)
    location = models.CharField(max_length=100, choices=CruiseDetailFinal.LOCATIONS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['cruise', 'room_type', 'location']),
            models.Index(fields=['user']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['cruise', 'room_number'], 
                name='unique_room_booking'
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.room_type} {self.room_number}"


class LogedInUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(default="")
    password = models.CharField(max_length=100)


class Household(models.Model):
    name = models.CharField(max_length=100)
    primary_contact = models.ForeignKey('GuestProfile', on_delete=models.SET_NULL, null=True, related_name='primary_household')
    created_at = models.DateTimeField(auto_now_add=True)


class GuestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    household = models.ForeignKey(Household, on_delete=models.SET_NULL, null=True, related_name='members')
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50)
    dietary_preferences = models.JSONField(default=dict)
    onboard_preferences = models.JSONField(default=dict)
    loyalty_points = models.IntegerField(default=0)
    referral_code = models.CharField(max_length=20, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)


class Product(models.Model):
    PRODUCT_TYPES = [
        ('DINING', 'Dining'),
        ('CONFERENCE', 'Conference Room'),
        ('WORKSHOP', 'Workshop'),
        ('SPA', 'Spa Treatment'),
        ('HOTEL', 'Hotel'),
        ('TRANSPORT', 'Transportation'),
        ('EXCURSION', 'Shore Excursion'),
        ('PACKAGE', 'Package'),
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    schedule = models.JSONField(null=True)
    is_allotment = models.BooleanField(default=False)
    allotment_details = models.JSONField(null=True)


class Package(models.Model):
    name = models.CharField(max_length=200)
    products = models.ManyToManyField(Product, through='PackageComponent')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()


class PackageComponent(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_mandatory = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)


class GroupBooking(models.Model):
    name = models.CharField(max_length=200)
    organizer = models.ForeignKey(GuestProfile, on_delete=models.CASCADE)
    cruise = models.ForeignKey(CruiseDetailFinal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BookingItinerary(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    embarkation_port = models.CharField(max_length=100)
    disembarkation_port = models.CharField(max_length=100)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)


class OnboardSpending(models.Model):
    guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE)
    cruise = models.ForeignKey(CruiseDetailFinal, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    

class SalesforceIntegration(models.Model):
    guest = models.OneToOneField(GuestProfile, on_delete=models.CASCADE)
    salesforce_id = models.CharField(max_length=100, unique=True)
    last_synced = models.DateTimeField(auto_now=True)
