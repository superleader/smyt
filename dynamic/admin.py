from django.contrib import admin
from dynamic.models import *

admin.site.register(globals().get('User'))
admin.site.register(globals().get('Room'))
