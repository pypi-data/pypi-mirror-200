#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Display Book Results with a Book Name and Book URL only """


from random import sample

from typing import List
from typing import Optional

from baseblock import BaseObject

from slackbot_helper.blocks.dto import book_emojis


class BookOnlyBlock(BaseObject):
    """ Display Book Results with a Book Name and Book URL only

    This is often useful when the 'book' is a short 2-3 page article

    View Sample Output:
        ???
    """

    def __init__(self,
                 emojis: Optional[List[str]] = None,
                 target_users: Optional[str] = None):
        """ Change Log

        Created:
            15-Nov-2022
            craigtrim@gmail.com
            *   created in pursuit of
                https://github.com/craigtrim/slackbot-helper/issues/2
        Updated:
            21-Nov-2022
            craigtrim@gmail.com
            *   fix concatendation defect
                https://github.com/craigtrim/slackbot-helper/issues/8

        Args:
            emojis (Optional[List[str]], optional): list of emojis to use in display block. Defaults to None.
                if left empty, will sample from 'book' themed slack emojis
            target_users (Optional[str], optional): the Slack User IDs to target with this response. Defaults to None.
                if left empty, the response will not target any specific Slack IDs
        """
        BaseObject.__init__(self, __name__)
        self._emojis = emojis
        self._target_users = target_users

    def _find_emoji(self) -> str:
        if self._emojis and len(self._emojis):
            return sample(self._emojis, 1)[0]
        return sample(book_emojis, 1)[0]

    @ staticmethod
    def _primary_text_only(primary_text: str,
                           book_button_text: str,
                           book_url: str) -> list:
        return [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': primary_text
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': book_button_text,
                            'emoji': True
                        },
                        'url': book_url
                    }
                ]
            }
        ]

    @staticmethod
    def _secondary_text(primary_text: str,
                        secondary_text: List[str],
                        book_button_text: str,
                        book_url: str) -> list:
        return [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': primary_text
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': secondary_text
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': book_button_text,
                            'emoji': True
                        },
                        'url': book_url
                    }
                ]
            }
        ]

    def process(self,
                primary_text: str,
                secondary_text: Optional[List[str]],
                book_url: str,
                book_name: str,
                book_button_text: str,
                slack_channel_id: str,
                slack_thread_ts: Optional[str] = None) -> dict:
        """ Entry Point

        Args:
            primary_text (str): the primary output text to display to the user
            secondary_text (Optional[List[str]]): the secondary output text for the user
            book_url (str): the S3 Chapter URL
            book_name (str): the name of the book (label form)
            book_button_text (str): the name to display on the button
            slack_channel_id (str): the Slack Channel ID
            slack_thread_ts (Optional[str], optional): the Slack Thread timestamp. Defaults to None.

        Returns:
            dict: the display block
        """

        emoji = self._find_emoji()

        if emoji and len(emoji):  # slackbot-helper/issues/8
            book_button_text = f'{emoji} {book_button_text}'

        # slackbot-helper/issues/8
        if self._target_users and len(self._target_users):
            primary_text = f'{self._target_users} {primary_text}'

        def decide() -> list:
            if secondary_text and len(secondary_text):
                return self._secondary_text(
                    book_url=book_url,
                    book_button_text=book_button_text,
                    primary_text=primary_text,
                    secondary_text=secondary_text)

            return self._primary_text_only(
                book_url=book_url,
                book_button_text=book_button_text,
                primary_text=primary_text)

        blocks = decide()

        d_event_outgoing = {
            'blocks': blocks,
            'channel': slack_channel_id,
            'thread_ts': slack_thread_ts,
        }

        return d_event_outgoing
