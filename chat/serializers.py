from rest_framework import serializers
from .models import ChatInteraction

class ChatInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInteraction
        fields = ["user","user_message", "bot_response", "timestamp"]
        read_only_fields = ["bot_response", "timestamp"]



class ChatInputSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000, required=True)

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value
    
    class Meta:
        model=ChatInteraction
        