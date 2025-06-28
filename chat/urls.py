from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chatbot, name="chatbot"),
    path("interactions/<str:period>/", views.get_interactions, name="get_interactions"),
]