from django.contrib import admin
from apps.posts.models import Post, RecordPage
from solo.admin import SingletonModelAdmin


admin.site.register(RecordPage, SingletonModelAdmin)
admin.site.register(Post)
