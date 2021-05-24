from django.core.validators import RegexValidator
from django.db import models


class Principal(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    message = models.CharField(max_length=500, null=False, blank=False)
    image = models.ImageField(null=False, blank=False, upload_to='static/images/principal',default='default.jpg')

    class Meta:
        verbose_name_plural = 'Principal'

    def __str__(self):
        return self.name
#
# class VicePrincipal(models.Model):
#     name = models.CharField(max_length=100, null=False, blank=False)
#     message = models.CharField(max_length=500, null=False, blank=False)
#     image = models.ImageField(null=False, blank=False, upload_to='static/images/vice',default='default.jpg')
#
#     class Meta:
#         verbose_name_plural = 'Vice Principal'
#
#     def __str__(self):
#         return self.name


class School(models.Model):

    about = models.CharField(max_length=300)
    image = models.ImageField(null=True, blank=True, upload_to='static/images/school', default='default_img.jpg')
    philosophy = models.CharField(max_length=200)
    academic_principal = models.CharField(max_length=200)
    facilities = models.CharField(max_length=200)
    # twitter_link = models.URLField(blank=True, null=True)
    # facebooK_link = models.URLField(blank=True, null=True)
    # linkedin_link = models.URLField(blank=True, null=True)
    # mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    # mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=False, null=True, unique=True)
    # email = models.EmailField(null=True,blank=True)
    # address = models.CharField(null=True,blank=True)
    # academic_history = models.CharField(null=True,blank=True)
    def __str__(self):
        return self.about[:20]

    class Meta:
        verbose_name_plural = 'School'



class Paragraph(models.Model):
    related = models.ForeignKey(School, on_delete=models.CASCADE)
    para = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.para



class Partner(models.Model):
    image = models.ImageField(null=False, blank=False, upload_to='static/images/partner',default='img_default.jpg')
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name
