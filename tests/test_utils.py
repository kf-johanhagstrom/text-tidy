
import pytest

import textstada
from textstada import Pipeline

def msg(t, e, r):
    return f"\nTested:   '{t}'\nExpected: '{e}'\nReceived: '{r}'\n"

def test_generate_pipeline_file():
    steps =[
        "remove_escapes",
        "space_sentencestops"
    ]

    expected = {
        "0": {'step': 'remove_escapes', 'kwargs': {}},
        "1": {'step': 'space_sentencestops', 'kwargs': {'stop_chars': '.;!?,:'}}
        }
    test = textstada.utils.generate_pipeline_file(steps)

    assert test==expected
