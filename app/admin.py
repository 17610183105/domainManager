from django.contrib import admin
from app import models
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin,ImportExportModelAdmin


admin.site.register(models.account)
admin.site.register(models.record)
admin.site.register(models.domainsite)

class domainResource(resources.ModelResource):
    class Meta:
        model = models.domain
        export_order = ('id','name','account','nsrecord','desc','ctime','mtime')

@admin.register(models.domain)
class domainAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin):
    list_display = ('id','name','account','desc','ctime','mtime')
    search_fields = ('name','account','nsrecord')
    date_hierarchy = 'ctime'
    resource_class = domainResource