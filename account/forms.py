from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth import models
from .models import TeacherUser, StudentUser
from django.utils.translation import activate, ugettext as _
from django.contrib.auth.models import Group

from result.models import Class


class RegisterUserForm(UserCreationForm):
    # group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff']
        # exclude = ('last_login',)


    def clean_password_confirm(self):
        password = self.cleaned_data['password1']
        password_confirm = self.cleaned_data.get('password2')

        print(password)
        print(password_confirm)
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return password_confirm

    # def clean_username(self, *args, **kwargs):
    #     username =  self.cleaned_data.get('username')
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     if email and User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(u'Email addresses must be unique.')

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     if commit:
    #         user.save()
    #     return user


class TeacherForm(forms.ModelForm):
    class Meta:
        model = TeacherUser
        fields = ('age', 'image', 'file', 'date_of_birth', 'teacher_identification')
        exclude = ('file', 'date_of_birth')



class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentUser
        fields = ('student_identity', 'classes')
        exclude = ('file', 'date_of_birth')
