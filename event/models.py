import os

from django.db import models
from account.models import TeacherUser, StudentUser


class Category(models.Model):
    title = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]

    class Meta:
        verbose_name_plural = "Events Categories"


class Event(models.Model):
    title = models.CharField(max_length=255)
    featured_image = models.ImageField(null=True, blank=True, upload_to='static/images/events', default='img_default.jpg')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    tags = models.CharField(max_length=100)
    teacher = models.ManyToManyField(TeacherUser)
    student = models.ManyToManyField(StudentUser)
    date_added = models.DateField(auto_now_add=True)
    date_edited = models.DateField(auto_now_add=True)
    featured = models.BooleanField()
    block = models.BooleanField()

    def __str__(self):
        return self.title[:50]

    def get_absolute_image(self):
        return os.path.join('/media', self.title)


class Image(models.Model):
    event = models.ForeignKey(Event, default=None, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='static/images/gallery', default='img_default.jpg')
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event.title
