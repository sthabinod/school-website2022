from django.shortcuts import render
from result.models import Class
from account.models import StudentUser, TeacherUser
from attendence.models import Attendance
from django.contrib import messages

def attendence(request):

    classes = Class.objects.all().distinct('class_name')
    if request.method == 'POST':
        class_ = request.POST.get('class')
        day = request.POST.get('day')
        date_time = request.POST.get('date_time')
        print(class_, day, date_time)
        class_teacher = TeacherUser.objects.get(class_teacher_of = class_)
        logged_in = TeacherUser.objects.get(id=request.user.teacheruser.id)
        if class_teacher == logged_in:

            print(class_teacher)
            students = StudentUser.objects.filter(classes = class_)
            print(students)
            data = {

            'class':class_,
            'day':day,
            'date_time':date_time,
            'students':students
        }
            return render(request, 'attendance/add_attendance.html',data)
        else:
            messages.error(request, "You are not authorized to add attedance for this class!")
    data = {

        'classes': classes
    }
    return render(request,'attendance/attendance.html', data)

def add_attendence(request):
    if request.method == 'POST':
        print('add')
        class_ = request.POST.get('class')
        day = request.POST.get('day')
        date_time = request.POST.get('date_time')
        print(class_, day, date_time)
        student = request.POST.getlist('names')
        attend = request.POST.getlist('is_present')
        print(student)
        print(attend)
        print(class_)
        for (name,is_present) in zip(student,attend):
            print(name, is_present)
            student_obj = StudentUser.objects.get(student_identity=name)
            class_obj = Class.objects.get(id=class_)

            Attendance.objects.create(student=student_obj,date_time=date_time, day=day,std_class=class_obj ,is_present=is_present)



    return render(request, 'attendance/add_attendance.html')