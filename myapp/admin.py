# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser


# # Register your models here.

# class CustomUserAdmin(UserAdmin):
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'city', 'state', 'address', 'phone')}

#         ),
#     )



# admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser  # Specify the model for the UserAdmin

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'city', 'state', 'address', 'phone', 'role')}
        ),
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'city', 'state', 'address', 'phone', 'role')}
        ),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
        ('Important dates', {
            'fields': ('last_login',)}
        ),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'city', 'state', 'phone', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)