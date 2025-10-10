from django.db import models
# from config.config import settings
from app.models.teacher import Teacher
from app.models.groups import Group
from app.models.homework import Homework

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True,null=True)
    homework = models.OneToOneField(Homework,on_delete=models.SET_NULL,blank=True,null=True,related_name='lesson')
    video_url = models.FileField(upload_to='media/video/', blank=True, null=True,default='media/video/default.mp4')
    image = models.ImageField(upload_to='media/image/', blank=True, null=True,default='media/image/default.jpg')
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='lessons')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='lessons')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # student_homework = models.ForeignKey('Homework',on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return self.title