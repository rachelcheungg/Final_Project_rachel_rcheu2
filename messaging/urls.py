from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="message-inbox"),
    path("<int:conversation_id>/", views.conversation_view, name="message-thread"),
    path("start/<int:sublease_id>/", views.start_conversation, name="start-conversation"),
]