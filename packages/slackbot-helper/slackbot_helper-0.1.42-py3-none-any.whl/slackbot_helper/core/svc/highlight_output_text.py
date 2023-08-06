#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Highlight the Portion of the Output Text that corresponds to the User Input Text """


from typing import Optional

from baseblock import BaseObject, TextUtils
from fast_sentence_tokenize import tokenize_text

from slackbot_helper.core.dmo import (ExactMatchHighlighter,
                                      FuzzyMatchHighlighter)


class HighlightOutputText(BaseObject):
    """ Highlight the Portion of the Output Text that corresponds to the User Input Text """

    def __init__(self):
        """ Change Log

        Created:
            6-Oct-2022
            craigtrim@gmail.com
            *   GRAFFL-CORE-0004
        Updated:
            12-Oct-2022
            craigtrim@gmail.com
            *   ported from owl-parser in pursuit of
                https://github.com/craigtrim/climate-bot/issues/8
        Updated:
            19-Oct-2022
            craigtrim@gmail.com
            *   ported from 'climate-bot' and renamed from 'output-text-highlighter'
        Updated:
            28-Oct-2022
            craigtrim@gmail.com
            *   refactor logic into domain components
        """
        BaseObject.__init__(self, __name__)
        self._exact_matching = ExactMatchHighlighter().process
        self._fuzzy_matching = FuzzyMatchHighlighter().process

    def process(self,
                text_1: str,
                text_2: str,
                enable_fuzzy_matching: bool = True) -> Optional[str]:
        """ Entry Point

        Args:
            text_1 (str): the baseline text string
            text_2 (str): the text string to modify (highlight)
            enable_fuzzy_matching (bool, optional): Enable Fuzzy Highlighting. Defaults to True.

        Returns:
            Optional[str]: a highlighted string (if any)
        """

        tokens_1 = tokenize_text(text_1.lower())
        tokens_2 = tokenize_text(text_2.lower())

        result = self._exact_matching(tokens_1=tokens_1,
                                      tokens_2=tokens_2,
                                      text_2=text_2)

        if result and result != text_1:
            return result

        if not enable_fuzzy_matching:
            return None

        result = self._fuzzy_matching(tokens_1=tokens_1,
                                      tokens_2=tokens_2,
                                      text_2=text_2)
        if result != text_1:
            return result

        return None
