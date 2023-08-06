# Slackbot Helper (slackbot-helper)

Contains Utility Functions to help deal with Slack Events and I/O

Slack Events structures are highly variable and deeply nested.

This algorithm performs consistent extraction of the core key:value pairs.

## Usage
Assume this incoming event:
```python
d_incoming = {
    "blocks": [
        {
            "block_id": "vz+U",
            "elements": [
                {
                    "elements": [
                        {
                            "type": "user",
                            "user_id": "U045HCSMG8K"
                        },
                        {
                            "text": " dead ahead!",
                            "type": "text"
                        }
                    ],
                    "type": "rich_text_section"
                }
            ],
            "type": "rich_text"
        }
    ],
    "channel": "C046DB9TLEL",
    "text": "<@U045HCSMG8K> dead ahead!",
    "ts": 1665195085.499959,
    "type": "app_mention",
    "user": "U04674UNRBJ"
}
```

Import the `normalize_event` function:
```python
from slackbot_helper import normalize_event

d_normalized = normalize_event(
    d_event=d_incoming,
    bot_ids=['U045HCSMG8K']
)
```

The `bot_ids` parameter is a list of all known **bot_ids** in your application.

The output of this function is:
```json
{
    "membership": "85e8d1eb_46c2_11ed_97a0_4c1d96716627",
    "analysis": {
        "commands": [],
        "meta_mode": "human2bot",
        "meta_type": "H2B_SINGLE",
        "text_1": "@U045HCSMG8K dead ahead!",
        "text_2": "dead ahead!",
        "user_all": ["U045HCSMG8K"],
        "user_source": "U04674UNRBJ",
        "user_target": "U045HCSMG8K"
    },
    "event": {
        "blocks": [
            {
                "block_id": "vz+U",
                "elements": [
                    {
                        "elements": [
                            {
                                "type": "user",
                                "user_id": "U045HCSMG8K"
                            },
                            {
                                "text": " dead ahead!",
                                "type": "text"
                            }
                        ],
                        "type": "rich_text_section"
                    }
                ],
                "type": "rich_text"
            }
        ],
        "channel": "C046DB9TLEL",
        "text": "<@U045HCSMG8K> dead ahead!",
        "ts": 1665195085.499959,
        "type": "app_mention",
        "user": "U04674UNRBJ"
    },
}
```

The `analysis` structure within the output contains the following fields of interest:
1. `commands`: Any Commands extracted from the text
2. `meta_mode`: The Mode of communication (`human2bot`, `human2human`, `bot2human`, `bot2bot`)
3. `meta_type`: The Type of communication (`H2B_SINGLE` means Human is addressing a Single bot)
4. `text_1`: The original text
5. `text_2`: The normalized text
6. `user_all`: All the user IDs addressed in the text
7. `source_user`: The Source User (responsible for sending the event)
8. `target_user`: The Target User (primary user responsible for receiving the event)
