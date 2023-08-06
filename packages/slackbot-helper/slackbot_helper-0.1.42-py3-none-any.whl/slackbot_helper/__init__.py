from typing import Optional

from .blocks import *
from .blocks.bp.result_block import ResultBlock
from .core import *
from .core.bp.normalize_incoming_event import NormalizeIncomingEvent
from .core.svc.highlight_output_text import HighlightOutputText


def highlight_text(text_1: str,
                   text_2: str) -> Optional[str]:
    """ Entry Point

    Args:
        text_1 (str): the baseline text string
        text_2 (str): the text string to modify (highlight)

    Returns:
        Optional[str]: a highlighted string (if any)
    """
    return HighlightOutputText().process(
        text_1=text_1,
        text_2=text_2,
        enable_fuzzy_matching=True)


def normalize_event(d_event: dict,
                    bot_ids: list) -> dict:
    """ Normalize the Incoming Slack Event

    Args:
        d_event (dict): the incoming Slack Event
        Sample Input:
            {
                'blocks': [
                    {
                        'block_id': 'vz+U',
                        'elements': [
                            ...
                        ],
                        'type': 'rich_text'
                    }
                ],
                'channel': 'C046DB9TLEL',
                'text': '<@U045HCSMG8K> dead ahead!',
                'ts': 1665195085.499959,
                'type': 'app_mention',
                'user': 'U04674UNRBJ'
            }
        bot_ids (list): a list of known Bot IDs

    Returns:
        dict: the normalized Slack event
        Sample Output:
            {
                'membership': '43fd5022_46c3_11ed_aca2_4c1d96716627'
                'event': {
                    ... copy of input event ...
                },
                'analysis': {
                    'commands': [],
                    'meta_mode': 'human2bot',
                    'meta_type': 'H2B_SINGLE',
                    'text_1': '@U045HCSMG8K dead ahead!',
                    'text_2': 'dead ahead!',
                    'user_all': ['U045HCSMG8K'],
                    'user_source': 'U04674UNRBJ',
                    'user_target': 'U045HCSMG8K'
                },
            }
    """
    return NormalizeIncomingEvent(bot_ids).process(d_event)


def create_outgoing_event(output_text: str,
                          d_event_incoming: dict) -> dict:
    """ Create an Outgoing Slack Event

    Args:
        output_text (str): the outgoing slack message
            -   The message to display in Slack to the consumer
        d_event_incoming (dict): the incoming slack event
            -   This is required to obtain the channel, thread timestamp (thread_ts) and input text (text)
            -   It was thought easier to pass the original (non-normalized) Slack event as a parameter value
                than to request these individual values

    Returns:
        dict: the outgoing slack event
    """
    return ResultBlock().text_block(
        output_text=output_text,
        d_event_incoming=d_event_incoming)
