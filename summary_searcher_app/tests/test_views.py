import json
import logging
import os

from django.test import TestCase

from summary_searcher_app.models import (InvertedIndex, Summary)
from utilities.summary_searcher_utilities import prepare_inverted_index

logger = logging.getLogger(__name__)


def add_summaries_to_db(file_data):
    for idx, a_summary in enumerate(file_data['summaries']):
        summary_ob = Summary()
        summary_ob.summary_text = a_summary['summary']
        summary_ob.summary_id = a_summary['id']
        summary_ob.title = file_data['titles'][idx]
        summary_ob.author = file_data['authors'][idx]['author']
        summary_ob.save()

    inverted_index = prepare_inverted_index(file_data['summaries'])
    for word in inverted_index:
        inverted_index_obj = InvertedIndex()
        inverted_index_obj.word = word
        inverted_index_obj.summaries = json.dumps(inverted_index[word])
        inverted_index_obj.save()


class SearchSummariesViewTest(TestCase):
    def create_summary(self, summary_id=1, author='Tiger',
                       title='Disha',
                       summary_text='Disha saves Tiger'):
        return Summary.objects.create(summary_id=summary_id,
                                      title=title,
                                      author=author,
                                      summary_text=summary_text)

    def create_inverted_index(self, word, summaries):
        return InvertedIndex.objects.create(word=word,
                                            summaries=json.dumps(summaries))

    def test_summary_search_view(self):
        file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'test_data1.json'

        with open(file_path) as summaries_file:
            file_data = json.load(summaries_file)
            add_summaries_to_db(file_data)

        resp = self.client.get('/search-summaries/', {'searchPhrase':
                                                      ['make you', 'at least'],
                                                      'count': 2})
        resp_to_compate = b'[{"summary": "The Book in Three Sentences: Practicing meditation and mindfulness will make you at least 10 percent happier.", "author": "Dan Harris", "query": "make you"}, {"summary": "The Book in Three Sentences: The 10X Rule says that 1) you should set targets for yourself that are 10X greater than what you believe you can achieve and", "author": "Grant Cardone", "query": "make you"}, {"summary": "The Book in Three Sentences: Practicing meditation and mindfulness will make you at least 10 percent happier.", "author": "Dan Harris", "query": "at least"}]'
        self.assertEqual(resp.status_code, 200)
        self.assertIn(resp_to_compate, resp.content)
