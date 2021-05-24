from django.contrib import admin
from django.utils.html import format_html

from .models import Event, Category, Image


class EventImageAdmin(admin.StackedInline):
    model = Image

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageAdmin]
    list_display_links = ('title',)
    list_display = ('title','start_date','end_date','category','venue','description','tags','block')
    list_filter = ('title',)
    search_fields = ('title','venue')
    list_per_page = 5
    raw_id_fields = ('category','teacher','student')
    autocomplete_fields = ('category','teacher','student')
    sortable_by = ('title',)
    class Meta:
        model = Event

@admin.register(Image)
class EventImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="200" height="150" />'.format(obj.image.url))

    image_tag.short_description = 'image'
    list_display = ('image_tag','event','date_created')
    list_per_page = 3
    date_hierarchy = ('date_created')
    search_fields = ('date_created',)
    autocomplete_fields = ('event',)
    raw_id_fields = ('event',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
