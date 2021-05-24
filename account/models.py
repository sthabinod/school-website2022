import uuid
from datetime import datetime, timezone
import datetime

from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser, User
from jsonschema import ValidationError
from django.contrib import messages

GENDER = [
    ('male', 'Male'),
    ('female', 'Female')
]


class TeacherUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(validators=[
            MaxValueValidator(60),
            MinValueValidator(18)
        ])
    file = models.FileField(upload_to='static/files', blank=True, null=True)
    image = models.ImageField(null=True, blank=False, upload_to='static/images/profiles',default='images/default.jpg')
    gender = models.CharField(choices=GENDER, max_length=10, null=False, blank=False)
    date_joined = models.DateField(auto_now=True)
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=False, null=True, unique=True)
    temporary_address = models.CharField(max_length=100, )
    permanent_address = models.CharField(max_length=100, )
    teacher_identification = models.CharField(max_length=100, null=True, blank=True, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    is_teaching = models.BooleanField(default=True)
    class_teacher_of = models.OneToOneField("result.Class", on_delete=models.CASCADE, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     try:
    #         if self.date_of_birth > datetime.date.today():
    #
    #             raise ValidationError("The date cannot be in the past!")
    #     except Exception:
    #         print("error")
    #     super(TeacherUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Teacher"
        # for migrations
        app_label = "account"
        managed = True

    def __str__(self):
        return f'{self.user}  |  {self.teacher_identification}'


class StudentUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True,validators=[
            MaxValueValidator(20),
            MinValueValidator(10)
        ])
    file = models.FileField(upload_to='static/files', blank=True, null=True)
    image = models.ImageField(null=True, blank=False, upload_to='static/images/profiles', default='images/default.jpg')
    gender = models.CharField(choices=GENDER, max_length=10, null=False, blank=False)
    date_of_admission = models.DateField(default=datetime.date)
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=False, null=True, unique=True)
    symbol_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    student_identity = models.CharField(max_length=100, null=False, blank=False, auto_created=True, unique=True)
    temporary_address = models.CharField(max_length=100, )
    permanent_address = models.CharField(max_length=100, )
    date_of_admission = models.DateField(auto_now=True)
    is_studying = models.BooleanField(default=True)
    classes = models.ForeignKey("result.Class", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Student"
        # for migrations
        app_label = "account"
        managed = True

    def __str__(self):
        return f'{self.user} {self.student_identity}'


class TeacherIdentification(models.Model):
    identification = models.CharField(max_length=10, null=False, blank=False, unique=True)
    used = models.BooleanField()

    def __str__(self):
        return self.identification


class StudentIdentification(models.Model):
    identification = models.CharField(max_length=10, null=False, blank=False, unique=True)
    used = models.BooleanField()

    def __str__(self):
        return self.identification
