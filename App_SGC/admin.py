from django.contrib import admin
from .models import CustomCondomino, CustomUser
# from .models import Usuario

# # Register your models here.

# admin.site.register(Usuario)

admin.site.register(CustomUser)
admin.site.register(CustomCondomino)