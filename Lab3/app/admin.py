from django.contrib import admin

from .models import *

admin.site.register(Item)
admin.site.register(Declaration)
admin.site.register(ItemDeclaration)
