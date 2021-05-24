# decorators
# built-in
import operator
from decimal import Decimal
import requests
# Misc
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# models
from account.models import StudentUser, TeacherUser
from event.models import Event
from news.models import News
from .models import Class, Exam, Subject, SubTeacher, SubjectClass, Result, Parent


# This method can be used to calculate grade as per percentage
def calculate_grade(percentage):
    if percentage < 20:
        return "E"
    elif 20 < percentage < 40:
        return "D"
    elif 40 < percentage < 50:
        return "C"
    elif 50 < percentage < 60:
        return "C+"
    elif 60 < percentage < 70:
        return "B"
    elif 70 < percentage < 80:
        return "B+"
    elif 80 < percentage < 90:
        return "A"
    elif 90 < percentage < 100:
        return "A+"
    else:
        print('Something went wrong')


# This method helps in calculating percentage as per grand total
def percentage(total, subjects):
    percentage = (total / (100 * subjects)) * 100
    return percentage


# This method is used to calulate grand total of student's result
def total(test_score, exam_score):
    total = test_score + exam_score
    return total


# This method is to show pass and failed student
def percent_status(percent):
    if 40 <= percent <= 100:
        return "Passsed"
    elif 40 > percent > 0:
        return "Failed"

# This method is used to calculate gpa from percent
def gpa(percent):
    return (percent / 100) * 4


@login_required(login_url='login')
def view_result(request):
    class_data = Class.objects.all()
    exams = Exam.objects.all().distinct('exam_term')
    if request.method == 'POST':

        # Getting post request data
        student_name = request.POST.get('name')
        exam_term = request.POST.get('exam_term')
        exam_year = request.POST.get('exam_date')
        student_class = request.POST.get('class')
        symbol_number = request.POST.get('sn')
        student_id = request.user.id
        try:

            # Filtering exam term data
            exam_term_check = Exam.objects.get(exam_term=exam_term, exam_year=exam_year)
            print(exam_term_check)
            try:
                # Filtering Symbol number of students
                sn_check = StudentUser.objects.get(symbol_number=symbol_number)
                list = []
                try:
                    # Checking if the result is published
                    if exam_term_check.is_publish:
                        try:
                            # Getting result as per student symbol number and exam details
                            result = Result.objects.filter(exam=exam_term_check, student_code=sn_check)
                            if result is not None:
                                # Total marks
                                total_exam_mark = 0
                                total_test_mark = 0

                                # Total
                                grand_total = 0
                                total_to_get = 0

                                # Percent
                                percent = 0
                                percent_stat = ''

                                # Grade
                                grade_got = None
                                grade_points = 0

                                # Parent, Student and teacher
                                parent = None
                                student = None
                                class_teacher = None

                                # Getting into result one by one
                                # For example getting marks, names, subject
                                for exam in result:
                                    # Marking
                                    exam_mark = int(exam.exam_score)
                                    test_mark = int(exam.test_score)
                                    total_mark = total(test_mark, exam_mark)

                                    # Grand total
                                    grand_total = total_mark + grand_total
                                    grand_total = round(grand_total, 2)

                                    # Getting number of subjects
                                    student = StudentUser.objects.get(symbol_number=symbol_number)

                                    try:
                                        # Getting parent's object
                                        parent = Parent.objects.get(student=student)
                                    except Exception:
                                        pass

                                    # Student classes
                                    class_out = student.classes

                                    try:
                                        # Getting teacher's object
                                        class_teacher = TeacherUser.objects.get(class_teacher_of=class_out)
                                    except Exception:
                                        pass

                                    try:
                                        # Getting subject related to class
                                        class_subject = SubjectClass.objects.filter(classes=class_out)
                                    except Exception:
                                        pass

                                    # Counting subject
                                    count_subject = class_subject.count()
                                    total_to_get = count_subject * 100

                                    # Percentage
                                    percent = percentage(grand_total, count_subject)
                                    percent_stat = percent_status(percent)
                                    percent = round(percent, 2)

                                    # Grade
                                    grade_got = calculate_grade(percent)
                                    grade_points = gpa(percent)
                                    grade_points = round(grade_points, 2)
                                data = {'result': result,
                                            'exams': exam_term_check,
                                            'exam_total': total_exam_mark,
                                            'test_total': total_test_mark,
                                            'grand_total': grand_total,
                                            'percentage': percent,
                                            'grade': grade_got,
                                            'student': student,
                                            'total_to_get': total_to_get,
                                            'status': percent_stat,
                                            'parent': parent,
                                            'grade_points': grade_points,
                                            'teacher': class_teacher
                                            }
                                return render(request, 'result/display_result.html', data)
                            else:
                                messages.error(request, "Result not found.")
                        except Exception:
                            messages.error(request, 'Result is not found')
                    else:
                        messages.error(request, "Result has not been published yet.")
                except Exception:
                    messages.error(request, "Result error!")
            except Exception:
                messages.error(request, "No such symbol number found!")
        except Exception:
            messages.error(request, "Exam details is not correct!")

        return redirect('view_result')
    else:
        print("Not a post request")
    return render(request, 'result/view_result.html', {'classes': class_data, 'exams': exams, })


@user_passes_test(operator.attrgetter('is_staff'))
def dashboard(request):
    teacher_user = request.user
    subjects = Subject.objects.all().count()
    classes = Class.objects.all().count()
    events = Event.objects.all().count()
    exams = Exam.objects.all().count()
    news = News.objects.all()[:4]
    exam = Exam.objects.all().distinct()
    first_term = 0
    second_term = 0
    third_term = 0
    try:
        first_term = Exam.objects.filter(exam_term="First Term").count()
        second_term = Exam.objects.filter(exam_term="Second Term").count()
        third_term = Exam.objects.filter(exam_term="Third Term").count()
    except Exception:
        pass
    data = {
        'teacher_user': teacher_user,
        'subjects': subjects,
        'classes': classes,
        'events': events,
        'exams': exams,
        'news': news,
        'exam': exam,
        'first_term': first_term,
        'second_term': second_term,
        'third_term': third_term
    }
    return render(request, 'result/main.html', data)


@login_required(login_url='login')
@user_passes_test(operator.attrgetter('is_staff'))
def result(request):
    exams = Exam.objects.all().distinct('exam_term')
    classes = Class.objects.all().distinct('class_name')
    data = {
        'exams': exams,
        'classes': classes
    }
    return render(request, 'result/result.html', data)


# raise permission error
class Student(object):
    pass


g_context = {}


@login_required(login_url='login')
@user_passes_test(operator.attrgetter('is_staff'))
def add_result(request):
    # getting all subjects
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:

            # getting subject from post request and get subject's object
            subject = request.POST.get('subject')
            subject_o = Subject.objects.get(subject_code=subject)
            try:
                # getting class from post request and get class's object
                classes = request.POST.get('class')
                class_check = Class.objects.get(id=classes)
                try:
                    term = request.POST.get('exam_term')
                    date = request.POST.get('exam_date')
                    # Checking exam details
                    exam_chk = Exam.objects.get(exam_term=term, exam_year=date)

                    try:
                        # Getting user and checking with teacher user
                        teacher = request.user.id
                        print('teacher', teacher)
                        teacher_check = TeacherUser.objects.get(user=teacher)
                        print(teacher_check)

                        try:
                            # Filter subject
                            subject_obj = Subject.objects.filter(subject_code=subject)
                            try:
                                test_score = request.POST.getlist('test_score')
                                exam_score = request.POST.getlist('exam_score')
                                student_name = request.POST.getlist('names')
                                try:
                                    for (mark, test, name) in zip(exam_score, test_score, student_name):

                                        try:
                                            student_test = StudentUser.objects.get(student_identity=name)
                                        except Exception:
                                            messages.error(request, "Result add: Student not found!")
                                        try:
                                            print(name)
                                            student_test = StudentUser.objects.get(student_identity=name)
                                            print(f'Test student {student_test}')
                                            print("here")
                                        except Exception:
                                            messages.error(request, "Result add: Student not found!")
                                        try:
                                            mark_dec = Decimal(mark)
                                            test_mark_dec = Decimal(test)
                                        except Exception:
                                            messages.error(request, "Result add: Marks cannot be empty")
                                            break
                                        try:
                                            result = Result.objects.create(subject_number=subject_o,
                                                                           teacher_code=teacher_check,
                                                                           student_code=student_test,
                                                                           exam_score=mark_dec,
                                                                           test_score=test_mark_dec,
                                                                           classes=class_check, exam=exam_chk)
                                            result.save()
                                            messages.success(request, "Result added successfully.")
                                        except Exception:
                                            messages.error(request, "Result add:Cannot repeat result!")
                                            break
                                    return redirect('add_result')
                                except Exception:
                                    messages.error(request, "error while inserting result")
                            except Exception:
                                messages.error(request, "Incorrect test and exam score")
                        except Exception:
                            messages.error(request, "Subject not matched!")

                    except Exception:
                        messages.error(request, "Teacher not found!")
                except Exception:
                    messages.error(request, "Exam error")
            except Exception:
                messages.error(request, "Class error")
        except Exception:
            messages.error(request, "Please select the subject!")
    else:
        print("Not a post request")
        # return render(request, 'result/add_result.html')

        return render(request, 'result/add_result.html', g_context)

    return render(request, 'result/add_result.html', g_context)


@login_required(login_url='login')
@user_passes_test(operator.attrgetter('is_staff'))
def send_result_data(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':

        # get post requests
        try:
            class_ = request.POST.get('class')
            term = request.POST.get('exam_term')
            print(term)
            date = request.POST.get('exam_date')

            # checking exam
            print('here')
            try:
                exam_check = Exam.objects.get(exam_term=term, exam_year=date)
                if exam_check.is_publish == False:

                    try:
                        # Getting logged in user
                        user = request.user
                        teacher_user = TeacherUser.objects.get(user=user)
                        print("POST REQUEST", class_, term, date)

                        try:
                            # Getting subject as per class
                            subject_c = SubjectClass.objects.filter(classes=class_)

                            list = []

                            try:
                                for su in subject_c:
                                    print(su)
                                    # Getting subject related teacher
                                    subc_teacher = SubTeacher.objects.filter(subject_fk=su, teacher_id=teacher_user)

                                    print(f'data {subc_teacher}')
                                    list.append(subc_teacher)

                                print(list)
                                if list:
                                    print("list have")
                                else:
                                    print("No data in list")

                                try:
                                    new_list = []
                                    for l in list:
                                        print(f'listing {l}')
                                        for l_data in l:
                                            # print()
                                            new_list.append(l_data.subject_fk.subject_code)

                                    print(f'new list{new_list}')
                                    try:
                                        # getting student names from classes
                                        names = StudentUser.objects.filter(classes=class_)
                                        print(names)
                                        if names:
                                            g_context = {
                                                'class_': class_,
                                                'exam_term': term,
                                                'exam_date': date,
                                                'names': names,
                                                'subject': subjects,
                                                'subjectss': list,
                                                'subjects': new_list
                                            }
                                            return render(request, 'result/add_result.html', g_context)
                                        elif not names:
                                            messages.error(request, 'There are no students in this class!')
                                            return redirect('result')
                                    except Exception:
                                        messages.error(request, "Class related students not found!")
                                except Exception:
                                    messages.error(request, "Cannot append on list of subjects!")
                            except Exception:
                                messages.error(request, "You do not have any subjects in this class!")
                        except Exception:
                            messages.error(request, "Subject and class not found!")
                    except Exception:
                        messages.error(request, "User is not authorized!")
                else:
                    messages.error(request, "Exam is already published!")
            except Exception:
                messages.error(request, "Exam details not found!")
        except Exception:
            messages.error(request, "Some post request not found!")
    else:
        messages.error(request, "No post request not found!")

    return redirect('result')


def result_report(request):
    teacher = request.user.id
    real_teacher = TeacherUser.objects.get(user=teacher)
    print(real_teacher)

    print(teacher)
    result = Result.objects.filter(teacher_code=real_teacher)
    result_count = Result.objects.filter(teacher_code=real_teacher).count()
    print(result)
    data = {
        'results': result,
        'count': result_count
    }
    return render(request, 'result/result_report.html', data)


def result_event(request):
    teacher = request.user.id
    print(teacher)
    real_teacher = TeacherUser.objects.get(user=teacher)
    print(real_teacher)
    events = Event.objects.filter(teacher=real_teacher)
    data = {
        'events': events
    }
    return render(request, 'result/result_event.html', data)


@user_passes_test(operator.attrgetter('is_superuser'))
def publish_result(request):
    exam = Exam.objects.filter(is_publish=False)
    data = {
        'exams': exam
    }
    return render(request, 'result/publish.html', data)


@user_passes_test(operator.attrgetter('is_superuser'))
def publish(request, id):
    exam = Exam.objects.get(id=id)

    # Checking if result is published or not
    if exam.is_publish is False:
        exam.is_publish = True
        exam.save()

        list = []
        list_mobile = []

        # sending mail
        student = StudentUser.objects.all()
        for st in student:
            list.append(st.user.email)

        # parent
        parent = Parent.objects.all()
        for p in parent:
            list.append(p.email_address)
        send_mail(
            'Result Published',
            'Please collect email',
            'stha.binod1000@gmail.com',
            list,
            fail_silently=False,
        )
        # sms
        parent = Parent.objects.all()
        for p in parent:
            list_mobile.append(p.mobile_number)



        r = requests.post("https://sms.aakashsms.com/sms/v3/send/",
            data={'auth_token': '1955db2f23a27d4e6226a604873c922614f72e6c94547d5035932efe8e9a4989',
                  'to': '9814927160',
                  'text': '<message to be sent>'})
        status_code = r.status_code
        response = r.text
        response_json = r.json()

    elif exam.is_publish is True:
        print("Published result cannot be changed!")
    return redirect('landing-page')
