from django.contrib import admin

from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
    fields = ('target', 'nickname', 'content', 'website')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CommentAdmin, self).save_model(request, obj, form, change)
