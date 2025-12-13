from django.urls import path, include
from . import views
from .views import ChampaignApartmentList

urlpatterns = [
    path("", views.ApartmentListView.as_view(), name='apartment-list'),
    path("signup/", views.signup_view, name="signup_urlpattern"),
    path("champaign/", ChampaignApartmentList.as_view(), name="champaign-apartments"),
    path("<str:name>/", views.ApartmentDetailView.as_view(), name='apartment-detail'),
]