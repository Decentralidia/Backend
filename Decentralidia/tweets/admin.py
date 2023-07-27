from django.contrib import admin
from tweets.models import Tweet

# Register your models here.
from .models import Tweet
 
@admin.register(Tweet)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in
Tweet._meta.get_fields()]
