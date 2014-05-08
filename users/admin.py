from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import User

from users.models import EmhUser

class EmhUserInline(admin.StackedInline):
    model = EmhUser
    can_delete = False
    verbose_name_plural = "emh_user"


class UserAdmin(UserAdmin):
    inlines = (EmhUserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)