from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import Location, Accommodation, SignUpRequest
from .forms import SignUpRequestForm
from django.core.exceptions import ValidationError

class LocationTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id="LOC001",
            title="Test Location",
            center=Point(1.0, 1.0),
            location_type="City",
            country_code="US",
            state_abbr="CA",
            city="Test City"
        )

    def test_location_creation(self):
        self.assertEqual(self.location.title, "Test Location")
        self.assertEqual(self.location.city, "Test City")
        self.assertEqual(self.location.country_code, "US")

    def test_location_str_method(self):
        self.assertEqual(str(self.location), "Test Location")

    def test_invalid_location_creation(self):
        location = Location(
            id="LOC002",
            title="", 
            center=Point(1.0, 1.0),
            location_type="Invalid",  
            country_code="ZZ",  
            state_abbr="XX", 
            city=""  
        )
        
        with self.assertRaises(ValidationError): 
            location.full_clean()  


class AccommodationTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id="LOC001",
            title="Test Location",
            center=Point(1.0, 1.0),
            location_type="City",
            country_code="US",
            state_abbr="CA",
            city="Test City"
        )
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Dynamically generate unique accommodation ID
        unique_id = f"BCC_{Accommodation.objects.count() + 1:03}"
        self.accommodation = Accommodation.objects.create(
            id=unique_id,
            title="Test Accommodation",
            country_code="US",
            usd_rate=100.00,
            amenities="Wi-Fi, Parking",
            center=Point(1.0, 1.0),
            location_id=self.location,
            user_id=self.user
        )

    def test_accommodation_creation(self):
        self.assertEqual(self.accommodation.title, "Test Accommodation")
        self.assertEqual(self.accommodation.usd_rate, 100.00)
        self.assertEqual(self.accommodation.amenities, "Wi-Fi, Parking")

    def test_accommodation_str_method(self):
        self.assertEqual(str(self.accommodation), "Test Accommodation")


class SignUpRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_sign_up_request_creation(self):
        signup_request = SignUpRequest.objects.create(user=self.user)
        self.assertEqual(signup_request.user.username, "testuser")
        self.assertFalse(signup_request.is_approved)


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Property Owners")

    def test_sign_up_view_post(self):
        response = self.client.post(
            reverse("sign_up"),
            {"username": "newuser", "email": "newuser@example.com", "password": "securepassword123"},
        )
        self.assertEqual(response.status_code, 302)

    def test_sign_up_view_get(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_success_view(self):
        response = self.client.get(reverse('sign_up_success'))
        self.assertEqual(response.status_code, 200)


class ApproveUserViewTestCase(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username="staff", is_staff=True, password="staffpass")
        self.normal_user = User.objects.create_user(username="normal", password="normalpass")

    def test_approve_user_as_staff(self):
        self.client.login(username="staff", password="staffpass")
        response = self.client.post(reverse("approve_user", args=[self.normal_user.id]))
        self.assertEqual(response.status_code, 403)
        self.normal_user.refresh_from_db()
        self.assertTrue(self.normal_user.is_staff)

    def test_approve_user_as_non_staff(self):
        self.client.login(username="normal", password="normalpass")
        response = self.client.post(reverse("approve_user", args=[self.staff_user.id]))
        self.assertEqual(response.status_code, 403)

class SignUpRequestFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
        }
        form = SignUpRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        data = {'username': ''}
        form = SignUpRequestForm(data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_password_mismatch(self):
        data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password321',  # Mismatched passwords
            'email': 'testuser@example.com'
        }
        form = SignUpRequestForm(data)
        self.assertFalse(form.is_valid())
