from django.contrib import admin
from .models import Post, Comment
from django.contrib.auth.models import User

class ArrayFieldListFilter(admin.SimpleListFilter):
    """Class for filtering posts by tags without problems"""
    title = 'Tags'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        tag = Post.objects.values_list('tag', flat=True)
        tag = [(tg, tg) for sublist in tag for tg in sublist if tg]  #The most odd and hard-to-understand list comprehension ever be
        tag = sorted(set(tag))
        return tag

    def queryset(self, request, queryset):
        """this method called after a click on a tag. Posts quryset will be filtered by clicked tag"""
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(tag__contains=[lookup_value])
        return queryset

class PostAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'text', 'tag', 'user', 'likes_amount', 'dislikes_amount']
    list_display = ('id', 'get_post_short_text', 'tag', 'user', 'likes_amount', 'dislikes_amount')
    list_filter = ['pub_date', 'user', ArrayFieldListFilter]  #There is a bug where tag query comes within brackets and with extra '
    search_fields = ['text']

admin.site.register(Post, PostAdmin)

