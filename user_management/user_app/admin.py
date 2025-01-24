from django.contrib import admin
from .models import users
# Register your models here.



@admin.register(users)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'name', 'name', 'is_approved', 'approval_status']
    list_filter = ['is_approved', 'approval_status']
    actions = ['approve_entries', 'reject_entries']

    def approve_entries(self, request, queryset):
        updated = queryset.update(is_approved=True, approval_status='Approved')
        self.message_user(request, f"{updated} entries were successfully approved.")
    approve_entries.short_description = "Approve selected entries"

    def reject_entries(self, request, queryset):
        updated = queryset.update(is_approved=False, approval_status='Rejected')
        self.message_user(request, f"{updated} entries were successfully rejected.")
    reject_entries.short_description = "Reject selected entries"

