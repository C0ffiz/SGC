from django.contrib import admin
from .models import CustomCondomino, CustomUser, CustomCondominio
# from .models import Usuario

# # Register your models here.

# admin.site.register(Usuario)

admin.site.register(CustomUser)
admin.site.register(CustomCondomino)
admin.site.register(CustomCondominio)