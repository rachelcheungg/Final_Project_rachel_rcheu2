from django.urls import path, include
from . import views

urlpatterns = [
    path("apartments/", views.ApartmentListView.as_view(), name='apartment-list'),
    path("<str:name>/", views.ApartmentDetailView.as_view(), name='apartment-detail'),
]