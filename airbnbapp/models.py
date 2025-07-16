from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICE = (
    ('guest', 'guest'),
    ('host', 'host'),
    ('admin', 'admin')
)

class UserProfile(AbstractUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=32)
    role = models.CharField(max_length=32, choices=STATUS_CHOICE, default='guest')
    phone_number = PhoneNumberField(null=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatar', null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.role},{self.username}, {self.last_name},{self.first_name}'

class Property (models.Model):
    PROPERTY_TYPE_CHOICES = (
    ('apartment', 'apartment'),
    ('house', 'house'),
    ('studio', 'studio')
    )
    owner = models.ForeignKey(UserProfile , on_delete=models.CASCADE,  related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    city = models.CharField(max_length=100)
    address = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    RULES_CHOICES=(
        ('no_smoking','no_smoking'),
        ('pets_allowed','pets_allowed'),
    )
    rules = models.CharField(choices=RULES_CHOICES)
    max_guests = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.city},{self.owner}'

    def get_avg_rating(self):
        rating=self.reviews_property.all()
        if rating.exists():
            return round(sum([i.rating for i in rating]) / rating.count(),1)
        return 0

    def get_count_reviews(self):
        return self.reviews_property.count()

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property}, {self.guest}'

class Review(models.Model):
    property = models.ForeignKey(Property,  on_delete=models.CASCADE,  related_name = 'reviews_property')
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property},{self.guest}'