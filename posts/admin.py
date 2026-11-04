from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "has_image", "created_at", "updated_at")
    list_filter = ("created_at", "author")
    search_fields = ("title", "content", "author__username")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("author",)

    @admin.display(boolean=True, description="Con imagen")
    def has_image(self, obj):
        return bool(obj.image)
