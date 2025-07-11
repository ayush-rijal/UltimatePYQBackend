from rest_framework import serializers
from .models import TodoList

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model=TodoList
        fields=['id','title','due_date','completed','user', 'description']
        read_only_fields=['user']


        