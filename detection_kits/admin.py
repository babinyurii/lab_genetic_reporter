from django.contrib import admin
from detection_kits.models import DetectionKit
from django.contrib.auth import get_user_model

class DetectionKitAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_created',
        'created_by',
    
    )

    filter_horizontal = ('linked_markers', )


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super(DetectionKitAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


    def add_view(self, request, form_url='', extra_context=None):
        data = request.GET.copy()
        data['created_by'] = request.user
        request.GET = data
        return super(DetectionKitAdmin, self).add_view(
            request, form_url='', extra_context=extra_context
        )

admin.site.register(DetectionKit, DetectionKitAdmin)