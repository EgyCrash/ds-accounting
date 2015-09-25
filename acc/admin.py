from django.contrib import admin
import autocomplete_light.shortcuts as al
# import every app/autocomplete_light_registry.py
al.autodiscover()
admin.autodiscover()
