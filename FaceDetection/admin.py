from django.contrib import admin

# Register your models here.
from . import models

class TodoListAdmin(admin.ModelAdmin):
    list_display = ("title",  "created") #    list_display = ("title",  "created", "due_date")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(models.ImageUploadModel)
admin.site.register(models.basket)
admin.site.register(models.User)
admin.site.register(models.memo)