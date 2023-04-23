from django.contrib import admin
from apps.posts.models import Post, Effect, RecordPage
from solo.admin import SingletonModelAdmin
from adminsortable.admin import SortableAdmin


admin.site.register(RecordPage, SingletonModelAdmin)
admin.site.register(Post)
admin.site.register(Effect, SortableAdmin)
