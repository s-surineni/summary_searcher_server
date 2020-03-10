import bisect
from collections import defaultdict
import json
import logging
import os
import re

logging.basicConfig(format='%(filename)s - %(lineno)d - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# file_data = None


def sanitize_text(text):
    text = text.lower()
    # TODO: Find out a way to remove empty string at last
    return re.split(r'[ \W]+', text)


def get_word_indices(summary_words):
    word_indices = defaultdict(list)
    for idx, a_word in enumerate(summary_words):
        word_indices[a_word].append(idx)
    return word_indices


def prepare_inverted_index(summaries):
    title_terms = {}

    for a_summary in summaries:
        summary_text = a_summary['summary']
        # This regex splits the summary on space and
        # punctuation like . , ? etc.,
        sanitized_text = sanitize_text(summary_text)
        title_terms[a_summary['id']] = sanitized_text

    logger.info('Done splitting summaries into words')
    for a_title_id, summary_words in title_terms.items():
        logger.info('Getting word indices for book {}'.format(a_title_id))
        title_terms[a_title_id] = get_word_indices(summary_words)

    logger.info('Preparing inverted index for words in all summaries')
    inverted_index = defaultdict(lambda: defaultdict(list))

    for a_file, words in title_terms.items():
        for a_word, positions in words.items():
            # print(a_word, positions)
            inverted_index[a_word][a_file] = positions
    return inverted_index


def look_for_word_in_summaries(word, inverted_index):
    if word in inverted_index:
        return [summary_id for summary_id in inverted_index[word].keys()]
    else:
        return []


def search_summaries(search_text, result_count,
                     filepath='data.json'):
    try:
        filepath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + filepath
        with open(filepath) as summaries_file:
            file_data = json.load(summaries_file)
            inverted_index = prepare_inverted_index(file_data['summaries'])
            search_text_sanitized = sanitize_text(search_text)
            # We will only find occurence of unique words
            search_text_sanitized_unique = set(search_text_sanitized)

            summary_words_map = defaultdict(lambda: {'count': 0, 'words': []})

            for word in search_text_sanitized_unique:
                summaries_containing_words = look_for_word_in_summaries(word,
                                                                        inverted_index)

                for a_summary_id in summaries_containing_words:
                    summary_words_map[a_summary_id]['count'] += 1
                    summary_words_map[a_summary_id]['words'].append(word)

            # Order summaries in the decreasing order of the number of word matches
            num_summaries_matched = len(summary_words_map)
            freq_summary_count = []
            for a_summary_id in summary_words_map:
                bisect.insort(freq_summary_count,
                              (summary_words_map[a_summary_id]['count'],
                               a_summary_id))

            max_word_summaries = []
            titles = file_data['titles']
            
            for a_summary in freq_summary_count[(num_summaries_matched) - 1:num_summaries_matched - 1 - result_count:-1]:
                max_word_summaries.append({titles[a_summary[1]]:
                                           summary_words_map[a_summary[1]]})
            return max_word_summaries
    except FileNotFoundError:
        logger.error('Make sure you\'ve included file in the folder: {}'
                     .format(os.path.dirname(os.path.realpath(__file__))))


if __name__ == '__main__':
    while True:
        search_text = input('''Please enter the text you want to search for:
Else exit() to exit:
> ''')
        if search_text == 'exit()':
            print('Bubye')
            break
        result_count = int(input('Please enter the number of matches you want: ').strip())

        print(search_summaries(search_text, result_count))
