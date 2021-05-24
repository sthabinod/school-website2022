from django.db import models

class News(models.Model):
    title = models.CharField(max_length=40)
    sub_title = models.CharField(max_length=100)
    category = models.CharField(max_length=40)
    image = models.ImageField(null=True, blank=True, upload_to='static/images/news', default='img_default.jpg')
    video = models.FileField(upload_to='static/videos', null=True, blank=True, )
    description = models.CharField(max_length=200, null=True, blank=True, )
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "News"