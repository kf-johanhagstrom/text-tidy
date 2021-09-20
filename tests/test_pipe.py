
import pytest

import textstada
from textstada import Pipeline

def msg(t, e, r):
    return f"\nTested:   '{t}'\nExpected: '{e}'\nReceived: '{r}'\n"


def test_pipeline():

    tests = [
        " Some bad  sentence.And bad stop",
        " some other   - text 100,000. e.g. 1,00. they've"
    ]

    expected = [
        "Some bad sentence. And bad stop.",
        "some other text 100000. eg 100. they have."
    ]

    pipe = Pipeline(pipe=textstada.FULLMONTY, verbose=True)
    pipe.text_input = tests
    pipe.run()
    assert pipe.text_output==expected


    pipe = Pipeline(tests[1], textstada.FULLMONTY, verbose=True)
    pipe.run()
    assert pipe.text_output==expected[1]
