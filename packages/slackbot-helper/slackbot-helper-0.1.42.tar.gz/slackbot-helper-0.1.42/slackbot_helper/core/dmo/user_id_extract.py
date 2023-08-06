#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract the User IDs from an Incoming Slack Event """


from pprint import pformat, pprint
from typing import List, Optional

from baseblock import BaseObject, Stopwatch

from slackbot_helper.core.dto import IncomingEvent, SlackIds


class UserIdExtract(BaseObject):
    """ Extract the User IDs from an Incoming Slack Event """

    def __init__(self) -> None:
        """ Change Log

        Created:
            24-Mar-2022
            craigtrim@gmail.com
            *   refactored out of 'parse-slack-events'
                https://github.com/grafflr/graffl-core/issues/241
        Updated:
            30-Mar-2022
            craigtrim@gmail.com
            *   minor refactoring
                https://github.com/grafflr/graffl-core/issues/246
        Updated:
            7-Oct-2022
            craigtrim@gmail.com
            *   refactored into 'slackbot-helper'
        Updated:
            13-Oct-2022
            craigtrim@gmail.com
            *   updated algorithm
                https://github.com/craigtrim/slackbot-helper/issues/1
        Updated:
            16-Nov-2022
            craigtrim@gmail.com
            *   fix defect in user-id-extraction
                https://github.com/craigtrim/slackbot-helper/issues/5
        """
        BaseObject.__init__(self, __name__)

    def _extract_ids(self,
                     message_text: str) -> Optional[List]:
        """ Extract User IDs from Message Text

        Sample Transformation Steps:
            1.  "@blattero hi how are you with @loqi today?"
            2.  ['', 'blattero hi how are you with ', 'loqi today?']
            3.  ['blattero hi how are you with ', 'loqi today?']
            4.  ['blattero', 'loqi']

        Args:
            message_text (str): the incoming message text

        Returns:
            list or None: a list of 0..* user ids
        """

        # GRAFFL-246-1084930282; no other users addressed
        if '@' not in message_text:
            return None

        if '<@' in message_text:
            message_text = message_text.replace('<@', '@')
            message_text = message_text.replace('>', '')

        lines = [x for x in message_text.split('@') if len(x)]
        lines = [x.split(' ')[0] for x in lines]
        lines = [x for x in lines if len(x) >= 10]

        return lines

    def _process(self,
                 d_event: IncomingEvent) -> Optional[List]:

        def log_error(message: str) -> None:
            self.logger.error('\n'.join([
                message,
                '\tStart Event Block ---------------------------',
                f'\t{pformat(d_event)}',
                '\t----------------------------- End Event Block']))

        # typically an event that comes from a user ...
        if 'blocks' in d_event:
            try:

                user_ids = []  # use list to preserve extraction order
                for block in d_event['blocks']:

                    if 'elements' in block:
                        for element in block['elements']:
                            if 'elements' not in element and 'text' in element:

                                def get_element_text() -> str:
                                    if type(element['text']) == str:
                                        return element['text']
                                    if type(element['text']) == dict and 'text' in element['text']:
                                        return element['text']['text']
                                    raise NotImplementedError

                                tokens = get_element_text().split()
                                if tokens[0].startswith('<@'):
                                    user_ids.append(tokens[0][2:-1])

                            else:

                                for inner in element['elements']:
                                    if inner['type'] == 'user' and inner['user_id'] not in user_ids:
                                        user_ids.append(inner['user_id'])

                    elif 'text' in block:  # slackbot-helper/issues/1
                        if 'text' not in block['text']:
                            log_error('Event Structure Not Recognized')
                            raise NotImplementedError

                        block_text = block['text']['text']
                        extracted_ids = self._extract_ids(block_text)
                        if extracted_ids:  # slackbot-helper/issues/5
                            [user_ids.append(x) for x in extracted_ids]

                    elif 'accessory' in block:  # this happens with formatted messages, like when giphy images are returned
                        pass  # TODO: can extract, but for now will pass

                if len(user_ids):
                    return user_ids

                # 20220331, GRAFFL-256-1085404768; no user ids is a normal situation
                return None

            except KeyError:
                log_error('Event Structure Parse Error for Blocks')
                raise ValueError

        # typically an event that comes from a bot ...
        if 'channel' in d_event:
            return self._extract_ids(d_event['text'])

        log_error('Event Structure Not Recognized')
        raise NotImplementedError

    @staticmethod
    def _cleanse(user_id: str) -> str:
        if '>' in user_id:
            user_id = user_id.replace('>', '')
        if '<' in user_id:
            user_id = user_id.replace('<', '')
        return user_id.strip()

    def process(self,
                d_event: IncomingEvent) -> SlackIds:
        """ Extract User Name

        Args:
            d_event (dict): the message text from the slack event
            Sample input:
                https://github.com/grafflr/graffl-core/issues/234

        Returns:
            str: the name of the user who asked the question
            Sample Output:
                U038QP8ND9P
        """

        sw = Stopwatch()

        results = self._process(d_event)

        if results:
            results = [self._cleanse(x) for x in results]
            results = [x.strip() for x in results if x and len(x)]

        if not results:
            results = []

        if self.isEnabledForDebug:

            if results:
                self.logger.debug('\n'.join([
                    'User ID Extraction Completed',
                    f'\tTotal Time: {str(sw)}',
                    f'\tTotal User IDs: {len(results)}']))
            else:
                self.logger.debug('\n'.join([
                    'User ID Extraction Completed',
                    f'\tTotal Time: {str(sw)}',
                    '\tNo User IDs Found']))

        return results
