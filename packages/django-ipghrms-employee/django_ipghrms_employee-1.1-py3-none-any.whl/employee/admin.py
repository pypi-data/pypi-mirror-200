from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(Employee)
admin.site.register(EmployeeUser)
admin.site.register(Status)
admin.site.register(CurEmpPosition)
admin.site.register(CurEmpDivision)
admin.site.register(Area)
admin.site.register(EmpSignature)

@admin.register(EmpYear)
class EmpYearAdmin(ImportExportModelAdmin):
	pass
