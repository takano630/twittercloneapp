from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account

class CustomUserAdmin(UserAdmin):
    model = Account
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('age',)}),)
    list_display = ['username', 'email', 'age']


admin.site.register(Account, CustomUserAdmin)
