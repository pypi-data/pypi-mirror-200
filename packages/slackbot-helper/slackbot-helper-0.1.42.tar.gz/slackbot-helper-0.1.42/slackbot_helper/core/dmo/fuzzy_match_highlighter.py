#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Highlight the Portion of the Output Text that generally corresponds to the User Input Text """


from typing import List, Optional, Text

from baseblock import BaseObject, TextUtils
from fast_sentence_tokenize import tokenize_text


class FuzzyMatchHighlighter(BaseObject):
    """ Highlight the Portion of the Output Text that generally corresponds to the User Input Text """

    def __init__(self):
        """ Change Log

        Created:
            28-Oct-2022
            craigtrim@gmail.com
            *   refactored out of 'highlight-output-text'
        Updated:
            16-Nov-2022
            craigtrim@gmail.com
            *   Fix null input defect
                https://github.com/craigtrim/slackbot-helper/issues/4
        """
        BaseObject.__init__(self, __name__)

    def _most_similar_phrase(self,
                             tokens_1: List[str],
                             tokens_2: List[str]) -> Optional[dict]:

        def high_score(some_d_results: dict) -> dict:
            score = max(list(some_d_results.keys()))
            return some_d_results[score]

        threshold = 0.80
        while threshold >= 0.75:

            i = 5
            while i >= 3:

                results = TextUtils.most_similar_phrase(
                    tokens_1=tokens_1,
                    tokens_2=tokens_2,
                    window_size=i,
                    score_threshold=threshold,
                    debug=False)

                if results and len(results):
                    return high_score(results)

                i -= 1

            threshold -= 0.01

    @staticmethod
    def _remove_punkt(input_text: str) -> str:

        def is_valid(token: str) -> bool:
            if len(token) == 1 and not token.isalpha():
                return False
            return True

        tokens = [x for x in input_text.split() if x and is_valid(x)]

        return ' '.join(tokens).strip()

    def process(self,
                tokens_1: List[str],
                tokens_2: List[str],
                text_2: str) -> Optional[str]:
        """ Entry Point

        Args:
            tokens_1 (str): the tokenized form of text-1
            tokens_2 (str): the tokenized form of text-2
            text_2 (str): the text string to modify (highlight)

        Returns:
            Optional[str]: a highlighted string (if any)
        """

        if not tokens_1 or not len(tokens_1):
            return None

        if not tokens_2 or not len(tokens_2):
            return None

        d_similar = self._most_similar_phrase(
            tokens_1=tokens_1,
            tokens_2=tokens_2)

        if not d_similar or not len(d_similar):
            return None

        text_2_lower = text_2.lower()
        # self._remove_punkt(d_similar['tokens_2'])
        common_phrase = d_similar['tokens_2']
        for x in [' .', ' !', ' ?', ' ,']:
            if x in common_phrase:
                common_phrase = common_phrase.replace(x, x.strip())

        if common_phrase not in text_2_lower:
            if self.isEnabledForWarning:
                self.logger.warning('\n'.join([
                    'Common Phrase Not Found in Text 2',
                    f'\tCommon Phrase: {common_phrase}',
                    f'\tText 2: {text_2_lower}']))
            return None

        x = text_2_lower.index(common_phrase)
        y = x + len(common_phrase)

        start = text_2[:x]
        mid = f'*{text_2[x:y]}*'
        end = text_2[y:]

        final = f'{start} {mid} {end}'
        while '  ' in final:
            final = final.replace('  ', ' ').strip()

        # remove improperly formatted punctuation
        # e.g., 'the end .' => 'the end.'
        for x in [' .', ' !', ' ?']:
            if x in final:
                final = final.replace(x, x.strip())

        return final
