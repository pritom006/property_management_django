from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SignUpRequest
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import SignUpRequestForm


@csrf_exempt
def sign_up_view(request):
    if request.method == "POST":
        form = SignUpRequestForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create sign-up request object (waiting for admin approval)
            sign_up_request = SignUpRequest.objects.create(user=user)
            # Add user to the 'Property Owners' group
            group = Group.objects.get(name="Property Owners")
            user.groups.add(group)
            # Automatically log in the user
            login(request, user)
            # Redirect to a success page
            return redirect("sign_up_success")
    else:
        form = SignUpRequestForm()
    return render(request, "sign_up.html", {"form": form})

# Success page after sign-up
def sign_up_success(request):
    return render(request, "sign_up_success.html")

# Admin assigns user as staff
@login_required
def approve_user(request, user_id):
    if request.user.is_staff:  # Only staff can approve users
        user = User.objects.get(id=user_id)
        user.is_staff = True  # Assign as staff
        user.save()
        return redirect('admin:auth_user_change', user_id=user.id)  # Redirect to admin user change page
    return HttpResponse("Unauthorized", status=403)


