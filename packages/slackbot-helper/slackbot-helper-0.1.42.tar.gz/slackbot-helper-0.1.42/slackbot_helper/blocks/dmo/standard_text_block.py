#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Format a Response into a "Slack Blocks" object """


from pprint import pformat
from typing import Optional

from baseblock import BaseObject


class StandardTextBlock(BaseObject):
    """ Format a Response into a "Slack Blocks" object """

    def __init__(self):
        """ Change Log

        Created:
            8-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/slackbot/issues/8
        Updated:
            17-Aug-2022
            craigtrim@gmail.com
            *   fix blank-text defect
                https://github.com/grafflr/slackbot/issues/99
        Updated:
            14-Sept-2022
            craigtrim@gmail.com
            *   change 'parse' attribute
                per https://api.slack.com/methods/chat.postMessage#formatting:
                -   By default, URLs will be hyperlinked.
                -   Set parse to none to remove the hyperlinks.
                -   The behavior of parse is different for text formatted with mrkdwn.
                -   By default, or when parse is set to none, mrkdwn formatting is implemented.
                -   To ignore mrkdwn formatting, set parse to full.
        Updated:
            7-Oct-2022
            craigtrim@gmail.com
            *   refactored out of slackbot and renamed from 'format-slack-response'
        Updated:
            15-Nov-2022
            craigtrim@gmail.com
            *   renamed from 'create-outgoing-event' in pursuit of
                https://github.com/craigtrim/slackbot-helper/issues/2
        Updated:
            16-Nov-2022
            craigtrim@gmail.com
            *   alt-text is a mandatory attribute with mandatory (non-null, non-empty) value
                https://github.com/craigtrim/slackbot-helper/issues/7
        Updated:
            21-Nov-2022
            craigtrim@gmail.com
            *   fix concatendation defect
                https://github.com/craigtrim/slackbot-helper/issues/8
        """
        BaseObject.__init__(self, __name__)

    def _no_links(self,
                  output_text: str) -> list:
        return [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',  # 20220914; use 'mrkdwn' to properly format <@UserId> statements
                    'text': output_text
                }
            }
        ]

    def _links(self,
               output_text: str) -> list:

        tokens = output_text.split('https:')
        url = f"https:{tokens[1].strip().replace(' ', '')}"

        text = tokens[0].strip()
        if not len(text):
            text = ' '  # COR-99; can't have blank text

        return [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': text
                },
                'accessory': {
                    'type': 'image',
                    'image_url': url,
                    'alt_text': text  # mandatory; slackbot-helper/issues/7
                }
            }
        ]

    def process(self,
                output_text: str,
                slack_channel_id: str,
                slack_thread_ts: Optional[str] = None,
                target_users: Optional[str] = None) -> dict:
        """ Entry Point

        Args:
            output_text (str): the outgoing slack message
            slack_channel_id (str): the Slack Channel ID
            slack_thread_ts (Optional[str], optional): the Slack Thread timestamp. Defaults to None.
            target_users (Optional[str], optional): the Slack User IDs to target with this response. Defaults to None.
                if left empty, the response will not target any specific Slack IDs

        Returns:
            dict: the display block
        """

        if not output_text or not len(output_text):
            return None

        if target_users and len(target_users):  # slackbot-helper/issues/8
            output_text = f'{target_users} {output_text}'

        def get_blocks() -> list:
            if 'https:' not in output_text:
                return self._no_links(output_text)
            return self._links(output_text)

        d_event_outgoing = {
            'blocks': get_blocks(),
            'channel': slack_channel_id,
            'thread_ts': slack_thread_ts
        }

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Constructed Outgoing Event',
                f'\tOutgoing Event:\n{pformat(d_event_outgoing)}']))

        return d_event_outgoing
