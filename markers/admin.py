from django.contrib import admin
from markers.models import SingleNucPol


class SingleNucPolAdmin(admin.ModelAdmin):
    list_display = ('rs', 'gene_name_short', 'nuc_var_1', 'nuc_var_2', 'gene_name_full', )
    list_display_links = ()
    search_fields = ('rs', 'gene_name_short', 'gene_name_full', )


admin.site.register(SingleNucPol, SingleNucPolAdmin)
