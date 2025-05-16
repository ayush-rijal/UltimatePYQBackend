from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'category', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)