from django.contrib import admin
from .models import LogicModel
# Register your models here.
class LogicModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    search_fields = ('name',)
    readonly_fields = ('count',)
    
admin.site.register(LogicModel, LogicModelAdmin)