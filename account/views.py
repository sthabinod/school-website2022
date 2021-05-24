from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# forms
from django.views import View

from config import settings
from result.models import Class
from .forms import TeacherForm, StudentForm, RegisterUserForm

# models
from .models import TeacherUser, StudentUser, TeacherIdentification, StudentIdentification
from django.contrib.auth.models import User, Group
# Misc
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError


# It is a function
# It is used for logging in the users
def login_user(request):
    if request.method == 'POST':
        # Getting from post request
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        # Checking if the user exists in database
        if User.objects.filter(username=username).exists() and User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            # Checking if user is active or not
            if user is None and request.user.is_active is False:
                messages.error(request, "User is not activated!")
                return redirect('login')
            else:
                # Calling login function and redirect to home page
                login(request, user)
                return redirect('landing-page')

        else:
            messages.error(request, 'Username or password does not matched!')
    else:
        print("This is not POST method")
    return render(request, 'account/login.html')


# It is a method for logging out the user
def logout_user(request):
    logout(request)
    return redirect('login')


# It is a method for rendering user's profile
@login_required
def profile(request):
    user = request.user
    return render(request, 'profiles/profile.html', {'user': user})


# It is a method used for sending token to email for user email verification
@login_required
def send_token_teacher(request, data):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    message = render_to_string('activate.html',
                               {
                                   'user': data,
                                   'domain': current_site.domain,
                                   'uid': urlsafe_base64_encode(force_bytes(data.id)),
                                   'token': account_activation_token.make_token(data)
                               }
                               )
    email_from = settings.EMAIL_HOST_USER
    list = [data.email]
    send_mail(email_subject, message, email_from, list)


# This method is used for registering teacher users
def user_teacher(request):
    # Calling Forms
    form_user = RegisterUserForm
    teacher = TeacherForm

    if request.method == 'POST':
        # Getting post request from forms
        new_form = RegisterUserForm(request.POST)
        teacher = TeacherForm(request.POST, request.FILES)
        try:
            # Getting post request
            exp = request.POST.get('age')
            teacher_id = request.POST.get('teacher_identification')
            firstname = request.POST.get("first_name")
            lastname = request.POST.get("last_name")
            emailvalue = request.POST.get("email")
            uservalue = request.POST.get("username")
            passwordvalue1 = request.POST.get("password1")
            passwordvalue2 = request.POST.get("password2")
            print(firstname, lastname, emailvalue, uservalue, passwordvalue1, passwordvalue2)
        except Exception:
            messages.error(request, 'Proper data is not available')

        # Checking password is matching or not
        if passwordvalue1 == passwordvalue2:
            # Checking if user already exists
            if User.objects.filter(username=uservalue).exists():
                messages.error(request, 'User already exists!')

            else:
                if User.objects.filter(email=emailvalue).exists():
                    messages.error(request, 'Email already exists!')
                else:
                    try:
                        # Checking teacher identification input with database
                        id_check = TeacherIdentification.objects.get(identification=teacher_id, used=False)
                        try:
                            # Creating object of User
                            data = User.objects.create_user(username=uservalue, password=passwordvalue1, email=emailvalue,
                                                            first_name=firstname,
                                                            last_name=lastname, is_active=False)
                            data.save()
                            try:
                                # Creating objects and saving Teacher User
                                u = TeacherUser.objects.create(user=data, age=exp, teacher_identification=teacher_id)
                                u.save()

                                # Setting teacher identification is used
                                id_check.used = True
                                id_check.save()

                                #  For sending token to verify the user mail
                                try:
                                    current_site = get_current_site(request)
                                    email_subject = 'Activate your account'
                                    message = render_to_string('activate.html',
                                                               {
                                                                   'user': data,
                                                                   'domain': current_site.domain,
                                                                   'uid': urlsafe_base64_encode(force_bytes(data.id)),
                                                                   'token': account_activation_token.make_token(data)
                                                               }
                                                               )
                                    email_from = settings.EMAIL_HOST_USER
                                    list = [data.email]
                                    send_mail(email_subject, message, email_from, list)

                                    messages.success(request, 'Account created successfully!')
                                    messages.success(request, 'Activate now to sign in!')
                                    return redirect('login')
                                except Exception:
                                    messages.error(request, 'Email sending error!')
                            except Exception:
                                messages.error(request, 'Teacher user creation error!')
                        except Exception:
                            messages.error(request, 'User creation error!')
                    except Exception:
                        messages.error(request, 'Identification error!')
        else:

            messages.error(request, 'Password does not matched!')
            print(new_form.errors)

    data = {
        'form': form_user,
        'teacher': teacher
    }
    return render(request, 'account/teacher_signup.html', data)


def user_student(request):
    form_user = RegisterUserForm
    student = StudentForm
    if request.method == 'POST':
        # Getting post request from forms
        new_form = RegisterUserForm(request.POST)
        teacher = TeacherForm(request.POST, request.FILES)
        try:
            # Getting post request
            exp = request.POST.get('student_identity')
            classes = request.POST.get('classes')
            class_obj = Class.objects.get(class_name=classes)
            student_id = request.POST.get('student_identity')
            firstname = request.POST.get("first_name")
            lastname = request.POST.get("last_name")
            emailvalue = request.POST.get("email")
            uservalue = request.POST.get("username")
            passwordvalue1 = request.POST.get("password1")
            passwordvalue2 = request.POST.get("password2")
            print(firstname, lastname, emailvalue, uservalue, passwordvalue1, passwordvalue2)
        except Exception:
            messages.error(request, 'Proper data is not available')

        # Checking password is matching or not
        if passwordvalue1 == passwordvalue2:
            # Checking if user already exists
            if User.objects.filter(username=uservalue).exists():
                messages.error(request, 'User already exists!')

            else:
                if User.objects.filter(email=emailvalue).exists():
                    messages.error(request, 'Email already exists!')
                else:
                    try:
                        # Checking teacher identification input with database
                        id_check = StudentIdentification.objects.get(identification=student_id, used=False)
                        # Creating object of User
                        try:
                            data = User.objects.create_user(username=uservalue, password=passwordvalue1, email=emailvalue,
                                                            first_name=firstname,
                                                            last_name=lastname, is_active=False)
                            data.save()
                            try:
                                # Creating objects and saving Teacher User
                                u = StudentUser.objects.create(user=data, classes=class_obj, student_identity=exp)
                                u.save()

                                # Setting teacher identification is used
                                id_check.used = True
                                id_check.save()

                                #  For sending token to verify the user mail
                                try:
                                    current_site = get_current_site(request)
                                    email_subject = 'Activate your account'
                                    message = render_to_string('activate.html',
                                                               {
                                                                   'user': data,
                                                                   'domain': current_site.domain,
                                                                   'uid': urlsafe_base64_encode(force_bytes(data.id)),
                                                                   'token': account_activation_token.make_token(data)
                                                               }
                                                               )
                                    email_from = settings.EMAIL_HOST_USER
                                    list = [data.email]
                                    send_mail(email_subject, message, email_from, list)

                                    messages.success(request, 'Account created successfully!')
                                    messages.success(request, 'Activate now to sign in!')

                                except Exception:
                                    messages.error(request, 'Email sending error!')
                            except Exception:
                                messages.error(request, 'Student user creation error!')
                        except Exception:
                            messages.error(request, 'User creation error!')
                    except Exception:
                        messages.error(request, 'Identification error!')
                    return redirect('login')

        else:
            print("Not working")
            messages.error(request, 'Student: Something went wrong!')
    classes = Class.objects.all().distinct()
    data = {
        'form': form_user,
        'student': student,
        'classes': classes
    }
    return render(request, 'account/student_signup.html', data)


# Activate user after click token link in gmail
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print('ud', uid)
            user = User.objects.get(pk=uid)
            print(user.id)
            print(user)
        except Exception as identifier:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_staff = True
            user.save()
            print(user.is_active)
            print("Working")
            messages.add_message(request, messages.INFO, 'Account activated successfully.')
            return redirect('login')
        else:
            return render(request, 'activation_failed.html', status=401)


class ActivateStudentAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print('ud', uid)
            user = User.objects.get(pk=uid)
            print(user.id)
            print(user)
        except Exception as identifier:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True

            user.save()
            print(user.is_active)
            print("Working")
            messages.add_message(request, messages.INFO, 'Account activated successfully.')
            return redirect('login')
        else:
            return render(request, 'activation_failed.html', status=401)


@login_required(login_url='login')
def update_profile_teacher(request):
    if request.method == 'POST':

        # Getting register user and teacher form with data
        user = RegisterUserForm(request.POST, instance=request.user)
        teacher = TeacherForm(request.POST, request.FILES, instance=request.user.teacheruser)

        # Checking if user is valid
        if user.is_valid() and teacher.is_valid():
            user.save()
            teacher.save()
            messages.success(request, "Account has been updated")
            return redirect('profile')
    else:
        user = RegisterUserForm(instance=request.user)
        teacher = TeacherForm(instance=request.user.teacheruser)

    return render(request, 'account/profile_update.html', {'user': user, 'profile': teacher})


@login_required(login_url='login')
def update_profile_student(request):
    if request.method == 'POST':

        # Getting register user and teacher form with data
        user = RegisterUserForm(request.POST, instance=request.user)
        student = StudentForm(request.POST, request.FILES, instance=request.user.studentuser)

        # Checking if user is valid
        if user.is_valid() and student.is_valid():
            user.save()
            student.save()
            messages.success(request, "Account has been updated")
            return redirect('profile')
    else:
        user = RegisterUserForm(instance=request.user)
        student = StudentForm(instance=request.user.studentuser)

    return render(request, 'account/profile_update.html', {'user': user, 'profile': student})


@login_required(login_url='login')
def change_password(request):

    # Passing user in PasswordChangeForm
    password_change = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        password_change = PasswordChangeForm(user=request.user, data=request.POST)

        # Checking if user is valid
        if password_change.is_valid():
            password_change.save()
            messages.success(request, "Password changed successfully!")
            return redirect('logout')
    else:
        pass
    return render(request, 'account/change_password.html', {'password_form': password_change})
