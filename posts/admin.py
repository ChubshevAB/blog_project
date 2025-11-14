from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ["author", "text", "created_at"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author_link", "created_at", "comments_count"]
    list_filter = ["created_at", "author"]
    search_fields = ["title", "content", "author__username"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [CommentInline]

    def author_link(self, obj):
        return format_html(
            '<a href="/admin/users/customuser/{}/change/">{}</a>',
            obj.author.id,
            obj.author.username,
        )

    author_link.short_description = "Автор"

    def comments_count(self, obj):
        return obj.comments.count()

    comments_count.short_description = "Комментарии"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("comments")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["text_preview", "author", "post", "created_at"]
    list_filter = ["created_at", "author"]
    search_fields = ["text", "author__username", "post__title"]
    readonly_fields = ["created_at", "updated_at"]

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Текст"
