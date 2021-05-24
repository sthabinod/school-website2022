from django.contrib import admin
from .models import Class, Subject, SubjectClass, StudentTeacher, Parent, ParentType, Result, SubTeacher, Exam


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('full_name','mobile_number','email_address','permanent_address','type','profession','relation','gender')
    search_fields = ('full_name','mobile_number','email_address','permanent_address','type','gender')
    autocomplete_fields = ('type',)
    raw_id_fields = ('type',)
    list_per_page = 10


@admin.register(ParentType)
class ParentTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_term', 'exam_year','is_publish')
    search_fields = ('exam_term',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # list_display = ('subject_code','classes','registration_date',)
    # list_filter = ('subject_code',)
    # search_fields = ('subject_code',)
    # raw_id_fields = ('classes',)
    # autocomplete_fields = ('classes',)
    pass



@admin.register(SubTeacher)
class SubTeachAdmin(admin.ModelAdmin):

    pass

@admin.register(SubjectClass)
class SubClassAdmin(admin.ModelAdmin):

    pass

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name','registration_date')
    search_fields = ('class_name',)



@admin.register(Result)
class ClassAdmin(admin.ModelAdmin):
    # list_display = ['subject_number', 'teacher_code', 'student_code', 'mark']
    pass