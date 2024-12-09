from django.contrib import admin
from  .models import Notes,Homework
# Register your models here.

admin.site.register(Homework)



@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'created_at')
