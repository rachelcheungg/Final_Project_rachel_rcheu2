from django.urls import path
from . import views

urlpatterns = [
    path("", views.goal_list, name="goal-list"),
    path("create/", views.create_goal, name="create-goal"),
    path("<int:pk>/update/", views.update_savings, name="update-savings"),
]