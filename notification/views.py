# from rest_framework import viewsets
# from .models import Notification
# from .serializers import NotificationSerializer

# class NotificationViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing notification instances.
#     """
#     # queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer
    

#     def get_queryset(self):
#         """
#         Optionally restricts the returned notifications to a given user,
#         by filtering against a `user` query parameter in the URL.
#         """
#         queryset = self.queryset
#         user = self.request.query_params.get('user', None)
#         if user is not None:
#             queryset = queryset.filter(user=user)
#         return queryset


# notifications/views.py

from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing notification instances.
    """
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        """
        Restrict the returned notifications to a given user by filtering
        against a `user` query parameter in the URL.
        """
        user = self.request.query_params.get('user', None)
        if user is not None:
            return self.queryset.filter(user_id=user)
        return self.queryset.none()
