from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation, AccommodationImage
#from django.contrib.gis.admin import OSMGeoAdmin



class AccommodationImageInline(admin.TabularInline):
    model = AccommodationImage
    extra = 1  # Show 1 extra empty field for new uploads
    fields = ['image']

# Admin for Location
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ['title', 'location_type', 'country_code', 'state_abbr', 'city']
    list_filter = ('location_type', 'country_code', 'state_abbr')

# Admin for Accommodation
class AccommodationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'country_code', 'bedroom_count', 'review_score', 
        'usd_rate', 'published', 'location_id', 'created_at', 'updated_at'
    )
    search_fields = ['title', 'country_code', 'location_id__title']
    list_filter = ('country_code', 'published', 'location_id')
    readonly_fields = ('user_id',)  # Make user_id always read-only
    inlines = [AccommodationImageInline]
    def get_queryset(self, request):
        """
        Superusers can view all accommodations.
        Staff admins can only view accommodations they own.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_staff:
            return qs.filter(user_id=request.user)
        return qs.none()  # Regular users have no access

    def get_form(self, request, obj=None, **kwargs):
        """
        Superusers have full access.
        Staff admins can only edit accommodations they own.
        """
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Restrict fields for staff admins when editing
            if obj and obj.user_id != request.user:
                for field in form.base_fields:
                    form.base_fields[field].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        """
        Automatically set the user_id to the logged-in staff admin on save.
        Superusers can modify any accommodation.
        """
        if not request.user.is_superuser:
            if change and obj.user_id != request.user:
                raise ValueError("You are not allowed to modify this accommodation.")
            # Set user_id to the current logged-in staff admin for new accommodations
            if not change:
                obj.user_id = request.user
        super().save_model(request, obj, form, change)

# Admin for LocalizeAccommodation
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'language', 'description')
    search_fields = ['property_id__title', 'language']
    list_filter = ('language',)

# Register models with custom admin interfaces
admin.site.register(Location, LocationAdmin)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
