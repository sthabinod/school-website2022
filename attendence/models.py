from django.db import models
from account.models import StudentUser
from result.models import Class

from django.utils.translation import ugettext as _

class Attendance(models.Model):
    DAY_OF_THE_WEEK = [
        ('1',_(u'Sunday')),
        ('2',_(u'Monday')),
        ('3',_(u'Tuesday')),
        ('4',_(u'Wednesday')),
        ('5',_(u'Thursday')),
        ('6',_(u'Friday')),
        ('7',_(u'Saturday')),

    ]

    student = models.ForeignKey(StudentUser, on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField()
    day = models.CharField(max_length=2, choices=DAY_OF_THE_WEEK)
    std_class = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    is_present = models.BooleanField()

    def __str__(self):
        return f'{self.student} {self.day} {self.date_time}'

    class Meta:
        unique_together = ('student', 'date_time', 'day', 'std_class')
