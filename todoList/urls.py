from django.urls import path
from .views import TodayTasksListView,TaskCreateView,TaskUpdateView,TaskDeleteView

urlpatterns = [
    path('today/',TodayTasksListView.as_view(),name='today-tasks'),
    path('create/',TaskCreateView.as_view(),name='create-task'),
    path('update/<int:id>/',TaskUpdateView.as_view(),name='update-task'),
    path('delete/<int:id>/',TaskDeleteView.as_view(), name='delete-task')
]
