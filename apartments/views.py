from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView, FormView
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from .models import Apartment
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from django.db.models import Q
from .models import Apartment

class ApartmentListView(ListView):
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

class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = "apartments/apartment_detail.html"
    context_object_name = "apartment"
    slug_field = "name"
    slug_url_kwarg = "name"