from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = "user"


class UserAdmin(UserAdmin):
    inlines = (UserInline, )
