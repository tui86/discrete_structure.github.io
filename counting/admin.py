from django.contrib import admin
from .models import CountingModel

class CountingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    search_fields = ('name',)
    readonly_fields = ('count',)

admin.site.register(CountingModel, CountingModelAdmin)