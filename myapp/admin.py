from django.contrib import admin
from .models import Users,Driver,Labour,ServiceProvider,Customer,Booking,Review,Complaint,Contact

admin.site.register(Driver)
admin.site.register(Labour)
admin.site.register(Customer)
admin.site.register(ServiceProvider)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Complaint)
admin.site.register(Contact)


from django.contrib.auth.admin import UserAdmin

@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register your models here.
