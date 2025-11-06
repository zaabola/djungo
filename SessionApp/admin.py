from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "conference", "session_day", "start_time", "end_time", "room")
    list_filter = ("conference", "session_day", "room")
    search_fields = ("title", "topic")
    ordering = ("session_day", "start_time")
    
    fieldsets = (
        ("Informations de base", {
            "fields": ("title", "topic", "conference")
        }),
        ("Planning", {
            "fields": ("session_day", "start_time", "end_time", "room")
        }),
    )