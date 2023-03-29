from django.contrib import admin
from .models import Sentence, Project

# Register your models here.
admin.site.register(Project)
admin.site.register(Sentence)