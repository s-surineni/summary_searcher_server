import json
import logging
import os

from utilities.summary_searcher_utilities import prepare_inverted_index
from django.core.management.base import BaseCommand, CommandError
from summary_searcher_app.models import Summary, InvertedIndex

logging.basicConfig(format='%(filename)s - %(lineno)d - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Loads database for local run'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file_path',
            nargs=1,
            help='The path at which JSON file is stored')

    def handle(self, *args, **options):
        file_path = 'data.json'
        if options['file_path']:
            file_path = options['file_path']

        try:
            file_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + file_path
            with open(file_path) as summaries_file:
                file_data = json.load(summaries_file)

                self.add_summaries_to_db(file_data)
                inverted_index = prepare_inverted_index(file_data['summaries'])
        except FileNotFoundError:
            logger.error('Make sure you\'ve included file in the folder: {}'
                         .format(os.path.dirname(os.path.realpath(__file__))))

    def add_summaries_to_db(self, file_data):
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
