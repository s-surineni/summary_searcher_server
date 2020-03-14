from djongo import models
from djongo.models.json import JSONField


class Summary(models.Model):
    summary_id = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    summary_text = models.CharField(max_length=5000)

    def __str__(self):
        return 'summary_id: {}, author: {}, title: {}'.format(self.summary_id,
                                                              self.author,
                                                              self.title)


class InvertedIndex(models.Model):
    word = models.CharField(max_length=30, primary_key=True)
    summaries = JSONField()

    def __str__(self):
        return 'word: {}, summaries: {}'.format(self.word,
                                                self.summaries)
