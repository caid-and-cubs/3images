from django.db import models
from django.utils import timezone


class GeneratedImage(models.Model):
    """Model for storing AI-generated images"""
    prompt = models.TextField(help_text="Text description used to generate the image")
    image_url = models.URLField(max_length=500, help_text="URL of the generated image")
    created_at = models.DateTimeField(default=timezone.now, help_text="When the image was generated")
    
    class Meta:
        ordering = ['-created_at']  # Show newest images first
        verbose_name = "Generated Image"
        verbose_name_plural = "Generated Images"
    
    def __str__(self):
        return f"Image #{self.id}: {self.prompt[:50]}{'...' if len(self.prompt) > 50 else ''}"
    
    @property
    def short_prompt(self):
        """Return a shortened version of the prompt for display"""
        return self.prompt[:100] + ('...' if len(self.prompt) > 100 else '')
