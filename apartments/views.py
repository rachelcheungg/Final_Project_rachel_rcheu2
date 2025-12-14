import requests
import math
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, FormView
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from .models import Apartment
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms_auth import UserSignUpForm
from django.views.generic import ListView
from django.db.models import Q
import json
from pathlib import Path
from django.conf import settings

DATA_FILE = Path(settings.BASE_DIR) / "apartments" / "data" / "champaign_apartments.json"

with open(DATA_FILE) as f:
    apartment_data = json.load(f)


class ApartmentListView(LoginRequiredMixin, ListView):
    model = Apartment
    template_name = "apartments/apartment_list.html"
    context_object_name = "apartments"

    def get_queryset(self):
        q = self.request.GET.get("q")
        queryset = super().get_queryset()
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(address__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class ApartmentDetailView(LoginRequiredMixin, DetailView):
    model = Apartment
    template_name = "apartments/apartment_detail.html"
    context_object_name = "apartment"
    slug_field = "name"
    slug_url_kwarg = "name"

def signup_view(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("apartment-list")
    else:
        form = UserSignUpForm()

    return render(request, "apartments/signup.html", {"form": form})


class ChampaignApartmentList(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("q", "").strip()
        page_number = request.GET.get("page", 1)

        apartments = []

        for feature in apartment_data.get("features", []):
            props = feature.get("properties", {})
            geom = feature.get("geometry", {})
            coords = geom.get("coordinates", [])

            if not coords or not coords[0]:
                continue

            try:
                lon, lat = coords[0][0]
            except (IndexError, TypeError, ValueError):
                continue

            name = (
                props.get("Complex_Name")
                or props.get("Building_Name")
                or "Unnamed Apartment"
            )
            address = props.get("Address", "")

            if query:
                if query.lower() not in name.lower() and query.lower() not in address.lower():
                    continue

            apartments.append({
                "name": name,
                "address": address or "Address not available",
                "units": props.get("Units"),
                "stories": props.get("Stories"),
                "latitude": lat,
                "longitude": lon,
            })

        paginator = Paginator(apartments, 25)
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "apartments/champaign_apartments.html",
            {
                "apartments": page_obj,
                "page_obj": page_obj,
                "query": query,
            },
        )