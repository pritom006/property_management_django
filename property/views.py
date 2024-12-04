from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SignUpRequest
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import SignUpRequestForm
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return HttpResponse("Go to the SignUp Page -> http://0.0.0.0:8000/sign-up")


@csrf_exempt
def sign_up_view(request):
    if request.method == "POST":
        form = SignUpRequestForm(request.POST)
        if form.is_valid():
            user = form.save()
            sign_up_request = SignUpRequest.objects.create(user=user)
            group = Group.objects.get(name="Property Owners")
            user.groups.add(group)
            login(request, user)
            return redirect("sign_up_success")
    else:
        form = SignUpRequestForm()
    return render(request, "sign_up.html", {"form": form})


def sign_up_success(request):
    return render(request, "sign_up_success.html")


@login_required
def approve_user(request, user_id):
    if request.user.is_staff:
        user = get_object_or_404(User, id=user_id)
        user.is_staff = True
        user.save()
        return redirect('admin:approve_user', user_id=user.id)
    return HttpResponseForbidden("Unauthorized")  # 403 status if unauthorized
