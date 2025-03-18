import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import User


@admin.action(description="Export to Excel (CSV)")
def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="export_{datetime.datetime.now().strftime("%Y-%m-%d")}.csv"'

    writer = csv.writer(response)
    fields = [field.name for field in User._meta.fields]
    writer.writerow(fields)

    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])

    return response


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'email', 'phone', 'salary', "created_at")
    actions = [export_to_excel]

