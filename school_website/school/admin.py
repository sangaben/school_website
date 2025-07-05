from django.contrib import admin
from .models import CarouselSlide

@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)

from django.contrib import admin
from .models import News, Subscriber
from .views import send_news_notification

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['send_notifications']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_published and form.changed_data:
            send_news_notification(obj)
    
    def send_notifications(self, request, queryset):
        for news in queryset:
            send_news_notification(news)
        self.message_user(request, f"Notifications sent for {queryset.count()} news items.")
    send_notifications.short_description = "Send notifications to subscribers"

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')


from django.contrib import admin
from .models import GalleryImage
from django.utils.html import format_html
from django.urls import reverse

class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title', 'category_display', 'upload_date', 'featured', 'admin_actions')
    list_filter = ('category', 'featured', 'upload_date')
    search_fields = ('title', 'description')
    list_editable = ('featured',)
    list_per_page = 20
    date_hierarchy = 'upload_date'
    readonly_fields = ('thumbnail_preview',)
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'thumbnail_preview', 'category', 'description', 'featured')
        }),
    )
    actions = ['make_featured', 'remove_featured']

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px; object-fit: contain;" />',
                obj.image.url
            )
        return "-"
    thumbnail_preview.short_description = 'Preview'

    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = 'Category'

    def admin_actions(self, obj):
        return format_html(
            '<div class="admin-actions">'
            '<a href="{}" class="button">Edit</a>'
            '</div>',
            reverse('admin:school_galleryimage_change', args=[obj.id])
        )
    admin_actions.short_description = 'Actions'

    def make_featured(self, request, queryset):
        queryset.update(featured=True)
        self.message_user(request, f"Marked {queryset.count()} images as featured.")
    make_featured.short_description = "Mark selected as featured"

    def remove_featured(self, request, queryset):
        queryset.update(featured=False)
        self.message_user(request, f"Removed {queryset.count()} images from featured.")
    remove_featured.short_description = "Remove selected from featured"

admin.site.register(GalleryImage, GalleryImageAdmin)