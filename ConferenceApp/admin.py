from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header="Conference Management admin 25/26"
admin.site.site_title="Conference dashboard"
admin.site.index_title="Conference management"
#admin.site.register(Conference)

class SubmissionInline(admin.StackedInline):
    model=Submission
    extra=1
    readonly_fields =("submission_id",)

@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    list_display =("name","theme","location","start_date","end_date","duration")
    ordering= ("start_date",)
    list_filter =("theme","location","end_date")
    search_fields =("name",)
    fieldsets = (
            ("Information General",{
                "fields": ("conference_id","name", "theme","description")
            }),

            ("Logistics" , {
                "fields": ("location","start_date","end_date")
            }),
    )
    readonly_fields= ("conference_id",)
    date_hierarchy = "start_date"
    #inlines = [SubmissionInline]
    def duration(self,objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date-objet.start_date).days
        return "RAS"
    duration.short_description="Duration (days)"

@admin.action(description="maquer comme payé")
def mark_as_payed(modeladmin,req,queryset):
    queryset.update(payed=True)

@admin.action
def mark_as_accepted(m,req,q):
    q.update(status="accepted")
class SubmissionAdmin(admin.ModelAdmin):
    list_display =("title","status","payed","submission_date")
    actions =[mark_as_payed,mark_as_accepted]
admin.site.register(Submission,SubmissionAdmin)