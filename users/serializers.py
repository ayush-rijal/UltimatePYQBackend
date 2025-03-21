from rest_framework import serializers
from .models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'first_name', 'last_name', 'email', 'profilePicture', 'is_active', 'is_staff', 'is_superuser']