from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls

urlpatterns = [
    path('student_user',views.user_student,name="user_student"),
    path('teacher_user',views.user_teacher,name="user_teacher"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name="activate"),
    path('activate_student/<uidb64>/<token>',views.ActivateStudentAccountView.as_view(),name="activate_student"),
    path('login',views.login_user,name="login"),
    path('logout',views.logout_user,name='logout'),
    path('reset', auth_views.PasswordResetView.as_view(template_name="account/reset_password.html"), name="reset"),
    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(template_name="account/reset_password_sent.html"),
         name="password_reset_done"),
    path('reset_password/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/reset_password_enter_form.html"),
         name="password_reset_confirm"),
    path('reset_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name="account/reset_password_done.html"),
         name="password_reset_complete"),
    path('profile',views.profile,name="profile"),
    path('update-profile-t',views.update_profile_teacher,name="update_teacher"),
    path('update-profile-s',views.update_profile_student,name="update_student"),
    path('change-pw', views.change_password, name="change-pw"),

]