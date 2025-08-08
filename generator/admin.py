from django.contrib import admin
from .models import GeneratedImage


@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    """Admin interface for GeneratedImage model"""
    list_display = ('id', 'short_prompt', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('prompt',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def short_prompt(self, obj):
        """Display shortened prompt in admin list"""
        return obj.prompt[:75] + ('...' if len(obj.prompt) > 75 else '')
    short_prompt.short_description = 'Prompt'
