from django.contrib import admin
from apps.about.models import AboutPage, Step
from solo.admin import SingletonModelAdmin

class StepAdmin (admin.TabularInline):
    model = Step
    extra = 0

class AboutPageAdmin (SingletonModelAdmin):
    inlines = [StepAdmin]

admin.site.register(AboutPage, AboutPageAdmin)
