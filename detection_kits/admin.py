from django.contrib import admin
from detection_kits.models import DetectionKit


class DetectionKitAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_created',
        'created_by',
    )

    filter_horizontal = ('markers', )



admin.site.register(DetectionKit, DetectionKitAdmin)