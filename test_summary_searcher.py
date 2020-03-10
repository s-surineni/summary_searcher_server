from summary_searcher import sanitize_text, get_word_indices, search_summaries


def test_split_summary():
    assert sanitize_text('a.b.c') == ['a', 'b', 'c']


def test_get_word_indices():
    assert get_word_indices(['the', 'thin', 'the']) == {'the': [0, 2],
                                                        'thin': [1]}


def test_search_summaries():
    result = search_summaries('will make you at', 'data2.json')
    expected = [{'Anything You Want': {'count': 4, 'words': ['make', 'you', 'at', 'will']}}, {'The Richest Man in Babylon': {'count': 1, 'words': ['you']}}]
    assert len(result) == len(expected)
    # Because I don't want to put restriction on order of the words matched
    for expected_match, result_match in zip(expected, result):
        assert expected_match.keys() == result_match.keys()
        summary_name = list(expected_match.keys())[0]
        assert (expected_match[summary_name]['count'] ==
                expected_match[summary_name]['count'])
        assert (set(expected_match[summary_name]['words']) ==
                set(expected_match[summary_name]['words']))
