from django.contrib import admin
from .models import Partner, Principal, School, Paragraph


@admin.register(Principal)
class PrincipalAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

# @admin.register(VicePrincipal)
# class ViceAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         num_objects = self.model.objects.count()
#         if num_objects >= 1:
#             return False
#         else:
#             return True


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 4:
            return False
        else:
            return True

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

@admin.register(Paragraph)
class AdminPara(admin.ModelAdmin):
    def image_tag(self, obj):
        return obj.description




