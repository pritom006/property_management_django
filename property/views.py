from django.shortcuts import render
from django.http import HttpResponse
from .models import Accommodation

from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
    DetailView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpRequestForm



# Create your views here.
def index(request):
    return HttpResponse("Hello world updated")


class AccommodationListView(LoginRequiredMixin, ListView):
    model = Accommodation
    template_name = "accommodation_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="Property Owners").exists():
            return qs.filter(user_id=self.request.user)
        return qs


def sign_up_view(request):
    if request.method == "POST":
        form = SignUpRequestForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to Property Owners group
            group = Group.objects.get(name="Property Owners")
            user.groups.add(group)
            login(request, user)  # Automatically log in the user
            return redirect("home")
    else:
        form = SignUpRequestForm()
    return render(request, "sign_up.html", {"form": form})