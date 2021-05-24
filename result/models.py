from django.core.validators import RegexValidator
from django.db import models
from account.models import TeacherUser, StudentUser
from django.contrib.auth.models import User
from psycopg2._psycopg import cursor
from django.core.validators import MaxValueValidator, MinValueValidator

from .utils import score_grade

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female')
]


class ParentType(models.Model):
    type = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type[:50]


class Parent(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=False, unique=True)
    email_address = models.EmailField(max_length=100, unique=True)
    temporary_address = models.CharField(max_length=100, )
    permanent_address = models.CharField(max_length=100, )
    type = models.OneToOneField(ParentType, models.DO_NOTHING)
    profession = models.CharField(max_length=50, default="Not Set")
    relation = models.CharField(max_length=50, default="Father")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name[:50]



class Class(models.Model):
    class_name = models.CharField(max_length=20, unique=True)
    registration_date = models.DateTimeField(auto_created=True,auto_now=True)
    # class_teacher = models.OneToOneField(TeacherUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name_plural = "Classes"


class Subject(models.Model):
    subject_code = models.CharField(max_length=100, unique=True)
    registration_date = models.DateTimeField(auto_created=True)
    # classes = models.ForeignKey(Class,on_delete=models.DO_NOTHING)
    # teacher = models.ManyToManyField(TeacherUser)

    # class Meta:
    #     unique_together = ('classes', 'subject_code',)

    def __str__(self):
        return self.subject_code

# subject code -> subjectclass -> subjectteacher
class SubjectClass(models.Model):
    subject_code = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    classes = models.ForeignKey(Class, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('subject_code', 'classes')
        verbose_name_plural = "Subject and Class"

    def __str__(self):
        return f'{self.subject_code} {self.classes}'


class SubTeacher(models.Model):
    subject_fk = models.ForeignKey(SubjectClass, on_delete=models.DO_NOTHING)
    teacher_id = models.ForeignKey(TeacherUser, on_delete=models.DO_NOTHING)
    pass
    class Meta:
        unique_together = ('subject_fk', 'teacher_id')
        verbose_name_plural = "Subject and Teacher"

    def __str__(self):
        return f'{self.subject_fk} {self.teacher_id}'

class Exam(models.Model):
    exam_year = models.DateField()
    exam_date_time = models.DateTimeField(auto_now_add=True)
    TERM = [
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term'),
    ]
    exam_term = models.CharField(max_length=100, choices=TERM)
    exam_class = models.ManyToManyField(Class)
    is_publish = models.BooleanField(default=False)

    def __str__(self):
        return 'Term: ' + '  ' + self.exam_term + ' |   Date:  ' + str(self.exam_year)


class StudentTeacher(models.Model):
    students_id = models.ForeignKey(StudentUser, on_delete=models.DO_NOTHING)
    teachers_id = models.ForeignKey(TeacherUser, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('students_id', 'teachers_id')
        verbose_name_plural = "Student and Teacher"

    def __str__(self):
        self.achieved_mark = "Tech Stu"





class Result(models.Model):
    subject_number = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher_code = models.ForeignKey(TeacherUser, on_delete=models.CASCADE)
    student_code = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    exam_score = models.DecimalField(decimal_places=2, max_digits=100,validators=[
            MaxValueValidator(90),
            MinValueValidator(0)
        ])
    test_score = models.DecimalField(decimal_places=2, max_digits=100, validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subject_number', 'teacher_code', 'student_code', 'exam', 'classes')
        verbose_name_plural = "Result"

    def __str__(self):
        return f' Student: {self.student_code} || Subject:  {self.subject_number} || Teacher: {self.teacher_code}  ||  Exam: {self.exam}'

    def total_score(self):
        return self.test_score + self.exam_score

    def grade(self):
        return score_grade(self.total_score())