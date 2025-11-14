from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OrganizingCommitee

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('affiliation', 'nationality', 'role')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('email', 'first_name', 'last_name', 'affiliation', 'nationality', 'role')
        }),
    )

@admin.register(OrganizingCommitee)
class OrganizingCommiteeAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'commitee_role', 'date_join')
    list_filter = ('commitee_role', 'conference')
    search_fields = ('user__username', 'user__email', 'conference__name')
