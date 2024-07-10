from django.contrib import admin
from detection_kits.models import (DetectionKit, 
                                DetectionKitMarkers, 
                                ConclusionsForSNP)
from django.contrib.auth import get_user_model


class DetectionKitMarkersInline(admin.TabularInline):
    model = DetectionKitMarkers
    extra = 5


class DetectionKitAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_created',
        'created_by',
    )

    inlines = (DetectionKitMarkersInline, )

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

class ConclusionsForSNPAdmin(admin.ModelAdmin):
    readonly_fields = ('det_kit_marker', 'genotype', )
    model = ConclusionsForSNP
    list_display = (
        'det_kit_marker',
        'genotype',
        'short_conclusion',
    )
    

    list_filter = ('det_kit_marker__detection_kit',
                    'det_kit_marker__marker' )

    def has_add_permission(self, request, obj=None):
        return False


    



admin.site.register(DetectionKit, DetectionKitAdmin)
admin.site.register(ConclusionsForSNP, ConclusionsForSNPAdmin)



