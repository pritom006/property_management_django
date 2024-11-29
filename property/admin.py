from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation
#from django.contrib.gis.admin import OSMGeoAdmin


# Admin for Location
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ['title', 'location_type', 'country_code', 'state_abbr', 'city']
    list_filter = ('location_type', 'country_code', 'state_abbr')

# Admin for Accommodation
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'published', 'location_id', 'created_at', 'updated_at')
    search_fields = ['title', 'country_code', 'location_id__title']
    list_filter = ('country_code', 'published', 'location_id')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name="Property Owners").exists():
            return qs.filter(user_id=request.user)
        return qs
# Admin for LocalizeAccommodation
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'language', 'description')
    search_fields = ['property_id__title', 'language']
    list_filter = ('language',)

# Register models with custom admin interfaces
admin.site.register(Location, LocationAdmin)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
