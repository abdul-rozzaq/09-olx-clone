from django.contrib import admin

from .models import Announcement, AnnouncementImage, Category


class AnnouncementImageInline(admin.StackedInline):
    model = AnnouncementImage
    fields = ["image"]
    max_num = 3


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "category", "is_active"]
    list_display_links = ["title"]
    inlines = [AnnouncementImageInline]


# admin.site.register(AnnouncementImage)
admin.site.register(Category)
