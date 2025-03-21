from rest_framework import generics,status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from .models import TodoList
from .serializers import TodoListSerializer
from django.utils import timezone
# from django.utils.timezone import make_aware
from datetime import datetime


class TodayTasksListView(generics.ListAPIView):
    serializer_class=TodoListSerializer
    
    def get_queryset(self):
        today_start=timezone.now().replace(hour=0,minute=0,second=0 , microsecond=0)
        today_end=timezone.now().replace(hour=23,minute=59,second=59,microsecond=999999)

        # today_start = make_aware(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
        # today_end = make_aware(datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999))

        tasks=TodoList.objects.filter(
            user=self.request.user,
            due_date__range=[today_start,today_end]
        )


        # print("Total tasks matching today's date:", tasks.count()) 

        # for task in tasks:
        # print(task.title,"-",task.due_date)

        return tasks

    

    def list(self,request,*args,**kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset,many=True)
        return Response({"data":serializer.data})
    
class TaskCreateView(generics.CreateAPIView):
    serializer_class=TodoListSerializer
    
    def perform_create(self,serializer):

        ##Custom behaviour can be added beofre saving the object
        serializer.save(user=self.request.user)


class TaskUpdateView(generics.UpdateAPIView):
    serializer_class=TodoListSerializer
    lookup_field='id'

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)

    def update(self,request,*args,**kwargs):
        partial=kwargs.pop('partial', False)
        instance=self.get_object()
        serializer=self.get_serializer(instance , data=request.data , partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TaskDeleteView(generics.DestroyAPIView):
    serializer_class=TodoListSerializer
    lookup_field='id' 
    # Lookup Field: id is used to identify the specific task to delete

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)    
    
    def destroy(self,request,*args,**kwargs):
        #Custom Logic before deletion(if needed)
        instance=self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Task deleted successfully"},status=status.HTTP_204_NO_CONTENT)