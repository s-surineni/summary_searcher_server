import json
from django.test import TestCase

from summary_searcher_app.models import (InvertedIndex, Summary)


class SummaryTest(TestCase):

    def create_summary(self, summary_id=1, author='Tiger',
                        title='Disha',
                        summary_text='Disha saves Tiger'):
        return Summary.objects.create(summary_id=summary_id,
                                      title=title,
                                      author=author,
                                      summary_text=summary_text)

    def test_summary_creation(self):
        s = self.create_summary()
        self.assertTrue(isinstance(s, Summary))
        self.assertEqual(str(s), 'summary_id: 1, author: Tiger, title: Disha')


class InvertedIndexTest(TestCase):

    def create_inverted_index(self, word, summaries):
        return InvertedIndex.objects.create(word=word,
                                      summaries=json.dumps(summaries))

    def test_summary_creation(self):
        summaries = {"1": [16], "6": [33], "9": [54], "26": [37], "30": [69]}
        ii = self.create_inverted_index('yourself', summaries)
        self.assertTrue(isinstance(ii, InvertedIndex))
        object_string = 'word: yourself, summaries: {"1": [16], "6": [33], "9": [54], "26": [37], "30": [69]}'
        self.assertEqual(str(ii), object_string)
