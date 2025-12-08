from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ApartmentListView.as_view(), name='apartment-list'),
    path("signup/", views.signup_view, name="signup_urlpattern"),
    path("<str:name>/", views.ApartmentDetailView.as_view(), name='apartment-detail'),
]