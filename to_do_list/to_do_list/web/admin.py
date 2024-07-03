from django.contrib import admin
from to_do_list.web.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
