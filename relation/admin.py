from django.contrib import admin
from .models import RelationModel
# Register your models here.

class RelationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    search_fields = ('name',)
    readonly_fields = ('count',)

admin.site.register(RelationModel, RelationModelAdmin)