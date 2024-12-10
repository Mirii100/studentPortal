from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Notes(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.title} {self.description}')
    class Meta:
        verbose_name_plural = "Notes"
        verbose_name='Notes'


    
class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    title=models.CharField(max_length=200)
    description=models.TextField()
    due_date=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_finised=models.BooleanField(default=False)



    def __str__(self):
        return f'{self.user.username} Homework - {self.description} - {self.due_date}'
    


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Todo - {self.title} - {self.is_finished}'


