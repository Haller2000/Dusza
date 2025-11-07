from django.contrib import admin
from .models import Player

# LEGEGYSZERŰBB MEGOLDÁS - csak regisztráld a modellt
admin.site.register(Player)