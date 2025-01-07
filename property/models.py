from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = geomodels.PointField()
    parent_id = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    location_type = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3)
    city = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField(null=True, blank=True)
    review_score = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = geomodels.PointField()
    images = ArrayField(models.CharField(max_length=300),
                        default=list, blank=True)
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE)
    amenities = models.JSONField()
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Accommodation'
        verbose_name_plural = 'Accommodations'

    def __str__(self):
        return self.title



    # def save(self, *args, **kwargs):
    #     if not self.user_id:
    #         from django.contrib.auth import get_user_model
    #         self.user_id = get_user_model().objects.first()
    #         # self.images = [shorten_url(img, 300) for img in self.images]
    #     super().save(*args, **kwargs)
    #     if self.pk:
    #         self.images = [
    #             image.image.url for image in self.accommodation_images.all()]
    #     super().save(*args, **kwargs)


    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = User.objects.first()  
        super().save(*args, **kwargs)
        self.images = [image.image.url for image in self.accommodation_images.all()]
        super().save(update_fields=['images'])  

    def clean(self):
        if self.usd_rate < 0:
            raise ValidationError("USD rate must be positive.")


# Signal to create a user and set user_id if not provided
@receiver(pre_save, sender=Accommodation)
def set_user_on_save(sender, instance, **kwargs):
    if instance.user_id is None:
        user = User.objects.create_user(
            username="defaultuser",
            password="defaultpassword",
            email="defaultuser@example.com"
        )
        instance.user_id = user
        print(f"Created new user {user.username} and set it to accommodation.")


class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        related_name="accommodation_images"
    )
    image = models.ImageField(upload_to='accommodations/images/')

    def __str__(self):
        return f"Image for {self.accommodation.title}"


# Signals to update the images field in Accommodation
@receiver(post_save, sender=AccommodationImage)
@receiver(post_delete, sender=AccommodationImage)
def update_accommodation_images(sender, instance, **kwargs):
    """
    Update the images array in the Accommodation model whenever an AccommodationImage is added or deleted.
    """
    accommodation = instance.accommodation
    if accommodation:
        accommodation.images = [
            image.image.url
            for image in accommodation.accommodation_images.all()
            if image.image
        ]
        accommodation.save()


class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(
        'Accommodation',
        on_delete=models.CASCADE,
        related_name='localizations'
    )
    language = models.CharField(max_length=2)
    description = models.TextField()
    policy = models.JSONField()

    def __str__(self):
        return f"{self.property_id.title} - {self.language}"


class SignUpRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sign-Up Request: {self.user.username}"
