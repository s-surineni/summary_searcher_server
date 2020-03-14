import json

from django.http import HttpResponse
from django.shortcuts import render

from .utilities import search_summaries

from .models import (InvertedIndex, Summary)

def search_summaries_view(request):
    search_phrase = request.GET['searchPhrase']
    count = int(request.GET['count'])
    result_summaries = search_summaries(search_phrase)

    summary_response = []
    for a_summary in result_summaries[:count]:
        summary_obj = Summary.objects.filter(summary_id=a_summary['summary_id'])[0]
        summary_dict = {'summary': summary_obj.summary_text,
                        'author': summary_obj.author,
                        'query': search_phrase}
        summary_response.append(summary_dict)
    return HttpResponse(json.dumps(summary_response))
