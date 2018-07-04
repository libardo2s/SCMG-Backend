from django.contrib import admin

# Register your models here.
from .models import PropietarioGanado, ImagenMarcaGanado, ComparacionModel, ComparacionItermediate, UsuarioPropietario

admin.site.register(PropietarioGanado)
admin.site.register(ImagenMarcaGanado)
admin.site.register(ComparacionModel)
admin.site.register(ComparacionItermediate)
admin.site.register(UsuarioPropietario)
