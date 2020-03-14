from django.contrib import admin
from .models import (InvertedIndex, Summary)

from utilities.summary_searcher_utilities import search_summaries


admin.site.register(InvertedIndex)
admin.site.register(Summary)
