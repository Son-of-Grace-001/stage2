from django.contrib import admin

# Register your models here.
from . models import User, Organisation

admin.site.register(User)
admin.site.register(Organisation)