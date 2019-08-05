from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('email',)}), ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'phone_number', 'password1', 'password2',)}),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('username', 'email', 'phone_number', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username', 'email')
    readonly_fields = ('last_login', 'created_at',)


admin.site.register(User, UserAdmin)
