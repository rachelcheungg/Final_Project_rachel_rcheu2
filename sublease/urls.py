from django.urls import path
from .views import (SubleaseListView, SubleaseDetailView, SubleaseCreateView,
                    SubleaseUpdateView, SubleaseDeleteView, SubleasePhotoUploadView)

urlpatterns = [
    path("", SubleaseListView.as_view(), name="sublease-list"),
    path("<int:pk>/", SubleaseDetailView.as_view(), name="sublease-detail"),
    path("create/", SubleaseCreateView.as_view(), name="sublease-create"),
    path("<int:pk>/edit/", SubleaseUpdateView.as_view(), name="sublease-edit"),
    path("<int:pk>/delete/", SubleaseDeleteView.as_view(), name="sublease-delete"),
    path("<int:pk>/photos/add/", SubleasePhotoUploadView.as_view(), name="sublease-add-photo"),
]