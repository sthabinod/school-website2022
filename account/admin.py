from django.contrib import admin
from django.utils.html import format_html

from .models import TeacherUser, StudentUser, StudentIdentification, TeacherIdentification

# Register your models here.

admin.site.site_header = "Koshi Higher Secondary School"
admin.site.site_title = "KEBS"
admin.site.index_title = "KEBS Admin Dashboard"


class StudentInLine(admin.TabularInline):
    model = StudentUser


@admin.register(TeacherUser)
class AdminTeacher(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))

    image_tag.short_description = 'image'
    date_hierarchy = 'date_joined'
    list_display = (
    'user', 'teacher_identification', 'image_tag', 'gender', 'date_joined', 'mobile_number', 'temporary_address')
    list_filter = ('user', 'teacher_identification')
    list_per_page = 3
    search_fields = ('teacher_identification', 'gender')
    list_display_links = ('teacher_identification', 'user')
    autocomplete_fields = ('user',)
    raw_id_fields = ('user',)
    readonly_fields = ('date_joined',)
    sortable_by = ('teacher_identification',)


@admin.register(StudentUser)
class AdminStudent(admin.ModelAdmin):
    list_display = ('symbol_number', 'student_identity', 'user', 'image', 'date_of_birth')
    # exclude = ('date_of_birth',)
    # fields = ('symbol_number','image','student_identity','date_of_birth','user','age')
    list_filter = ('symbol_number', 'student_identity')
    list_editable = ('user',)
    list_per_page = 3
    search_fields = ('symbol_number', 'student_identity',)
    list_display_links = ('date_of_birth', 'student_identity')
    # prepopulated_fields = {"slug":("symbol_number",)}
    preserve_filters = False
    autocomplete_fields = ('user',)
    ordering = ('student_identity',)
    raw_id_fields = ('user',)
    readonly_fields = ('image',)
    sortable_by = ('symbol_number',)
    view_on_site = False

    # fieldsets = (

    #     ('Unique Numbers',{'fields':('symbol_number','student_identity',)}),
    # )

    def birth_date(self, obj):
        return obj.date_of_birth

    birth_date.empty_value_display = '???'


# Admin Customization

@admin.register(TeacherIdentification)
class AdminTeacherID(admin.ModelAdmin):
    list_display = ('identification', 'used')


@admin.register(StudentIdentification)
class AdminStudentID(admin.ModelAdmin):
    list_display = ('identification', 'used')
