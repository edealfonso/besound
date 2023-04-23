from django.contrib import admin
from apps.home.models import HomePage
from solo.admin import SingletonModelAdmin


admin.site.register(HomePage, SingletonModelAdmin)
