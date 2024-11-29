from django.urls import path
from property.views import *

urlpatterns = [
    path("", index, name='home'),
    path("sign-up/", sign_up_view, name="sign_up"),
    path("accommodations/", AccommodationListView.as_view(), name="accommodation_list"),
]