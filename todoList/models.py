from django.db import models
from users.models import UserAccount

class TodoList(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=1000,default="Your Description")
    due_date=models.DateField()
    completed=models.BooleanField(default=False)
    user=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name="tasks")

    class Meta:
        db_table = 'todo_list'

    def __str__(self):
        return self.title   
     
