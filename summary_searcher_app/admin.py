from django.contrib import admin
from .models import (InvertedIndex, Summary)


admin.site.register(InvertedIndex)
admin.site.register(Summary)
