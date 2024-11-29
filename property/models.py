from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import JSONField

class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # Primary key, string (max 20 characters)
    title = models.CharField(max_length=100)  # Location name, required field
    center = geomodels.PointField()  # Geolocation (PostGIS Point field)
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # Foreign key to itself for hierarchical nesting
    location_type = models.CharField(max_length=20)  # Type of location (e.g., continent, country, state, city)
    country_code = models.CharField(max_length=2)  # ISO country code (max 2 characters)
    state_abbr = models.CharField(max_length=3)  # State abbreviation (max 3 characters)
    city = models.CharField(max_length=30)  # City name (max 30 characters)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for update

    def __str__(self):
        return self.title



class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # Primary key, string (max 20 characters)
    feed = models.PositiveSmallIntegerField(default=0)  # Feed number, unsigned small integer, default is 0
    title = models.CharField(max_length=100)  # Accommodation name, required field
    country_code = models.CharField(max_length=2)  # ISO country code (max 2 characters), required
    bedroom_count = models.PositiveIntegerField(null=True, blank=True)  # Number of bedrooms, unsigned integer
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # Review score, numeric (1 decimal place)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Price rate in USD, numeric (2 decimal places)
    center = geomodels.PointField()  # Geolocation (PostGIS Point field)
    images = ArrayField(models.CharField(max_length=300), default=list)  # Array of image URLs, default is an empty list
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE)  # Foreign key to Location model
    amenities = models.JSONField()  # JSONB array for amenities, each amenity max 100 characters
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User model (auth_user)
    published = models.BooleanField(default=False)  # Published flag, default is false
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp, auto updated on create
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp, auto updated on update

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically set the logged-in user if it's not already set
        if not self.user_id:
            from django.contrib.auth import get_user_model
            self.user_id = get_user_model().objects.first()  # Use the first user as a fallback if no user is provided
        super().save(*args, **kwargs)

# Signal to create a user and set user_id if not provided
@receiver(pre_save, sender=Accommodation)
def set_user_on_save(sender, instance, **kwargs):
    if instance.user_id is None:
        # Automatically create a user if user_id is not provided
        user = User.objects.create_user(
            username="defaultuser",  # Use a fallback username
            password="defaultpassword",  # Use a default password
            email="defaultuser@example.com"  # Use a fallback email
        )
        instance.user_id = user
        print(f"Created new user {user.username} and set it to accommodation.")




class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incremented primary key
    property_id = models.ForeignKey(
        'Accommodation',  # References the Accommodation model
        on_delete=models.CASCADE,  # Deletes localization if the accommodation is deleted
        related_name='localizations'  # Allows reverse relation lookup
    )
    language = models.CharField(max_length=2)  # Language code (max 2 characters)
    description = models.TextField()  # Localized description
    policy = models.JSONField()  # JSONB dictionary for policy (e.g., {"pet_policy": "value"})

    def __str__(self):
        return f"{self.property_id.title} - {self.language}"



class SignUpRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sign-Up Request: {self.user.username}"