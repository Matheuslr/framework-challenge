from django.contrib import admin

from user.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
    )


admin.site.register(User, UserAdmin)
