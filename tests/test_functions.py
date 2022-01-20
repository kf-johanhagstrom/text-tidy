import re
import pytest

import texttidy


def msg(t, e, r):
    return f"\nTested:   '{t}'\nExpected: '{e}'\nReceived: '{r}'\n"

def run_test(func, tests, *args, **kwargs):
    for test, expected in tests:
        output = func(test, *args, **kwargs)
        assert output == expected, msg(test, expected, output)

def run_list_test(func, tests, *args, **kwargs):
    # Test lists as inputs
    test = [i[0] for i in tests]
    expected = [i[1] for i in tests]
    output = func(test, *args, **kwargs)
    assert output == expected, msg(test, expected, output)


def test_single_space():
    tests = [
        ('hello  world', 'hello world'),
        ('hello   world', 'hello world'),
        (' hello world ', 'hello world'),
        (' hello world', 'hello world'),
        ('hello  world ', 'hello world')
    ]
    f = texttidy.single_space
    run_test(f, tests)
    run_list_test(f, tests)


def test_space_sentencestops():
    tests = [
        ('Bad stop.Good stop.', 'Bad stop. Good stop.'),
        ('Bad stop   .. Good stop.', 'Bad stop.. Good stop.'),
        ('100.00', '100.00'),
        ('hello .  world.', 'hello.  world.')
        ]
    f = texttidy.space_sentencestops
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_numerical_commas():
    tests = [
        ('1,000,000', '1000000'),
        ('100,0', '1000'),
        ('123,456.00', '123456.00')
    ]
    f = texttidy.remove_numerical_commas
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_dashes():
    tests = [
        ('COVID-19', 'COVID19'),
        ('one-to-one', 'one-to-one'),
        ('5-10', '5-10'),
        ('hello - world', 'hello  world'),
        ('hello - - world', 'hello   world'),
        ('hello -  - world', 'hello    world'),
        ('hello  world', 'hello  world'),
        ('hello  – - world', 'hello    world'),
        ('- hello world', ' hello world'),
        ('1-to-1', '1-to-1'),
        ('hello:-world', 'hello: world')
    ]
    f = texttidy.remove_dashes
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_bullets():
    tests = [
        ('• hello world', 'hello world'),
        (' • hello world', 'hello world'),
        ('• hello world  • hello world', 'hello world. hello world'),
        ('○ hello world', 'hello world'),
        ('● hello world', 'hello world'),
        ('· hello world.', 'hello world.')
    ]
    f = texttidy.remove_bullets
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_escapes():
    tests = [
        (' \n hello world \n hello world', 'hello world.  hello world'),
        ('\r hello world \t', 'hello world'),
    ]
    f = texttidy.remove_escapes
    run_test(f, tests)
    run_list_test(f, tests)


def test_add_fullstop():
    tests = [
        ('hello world', 'hello world.'),
        ('hello world.', 'hello world.'),
        ('hello world ', 'hello world.'),
        ('hello world. ', 'hello world.'),
        ('hello world?', 'hello world?'),
        ('hello world;::', 'hello world.'),
        ('hello world!;::', 'hello world!'),
        ('hello world - ', 'hello world.')
        ]
    f = texttidy.add_fullstop
    run_test(f, tests)
    run_list_test(f, tests)


def test_replace_contractions():
    tests = [
        ("I shouldn't have", "I should not have"),
        ("who'd be", "who would be"),
        ("wouldn't've", "would not have"),
        ("dont be silly", "do not be silly"),
        ("I'll not replace well nor ill", "I will not replace well nor ill")
        ]
    f = texttidy.replace_contractions
    run_test(f, tests)
    run_list_test(f, tests)


def test_clean_quote_chars():
    tests = [
        (r"‘Some bad quote’ and apos´s", "'Some bad quote' and apos's"),
        (r"“Bad double quotes”", '"Bad double quotes"')
        ]
    f = texttidy.clean_quote_chars
    run_test(f, tests)
    run_list_test(f, tests)


def test_replace_latin_abbrevs():
    tests = [
        ("this is e.g. edge. e. g.  be. g.", "this is eg edge. eg  be. g."),
        ("e.g.", "eg"),
        ("e.g", "eg"),
        ("I.E.", "ie")
        ]
    f = texttidy.replace_latin_abbrevs
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_pronouns():
    tests = [
        ("He went", "went"),
        ("what he wanted", "what wanted"),
        ("they've needed.", "'ve needed.")
        ]
    f = texttidy.remove_pronouns
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_punctuation():
    tests = [
        ('This is [a] "string". Hello world!', "This is a string . Hello world!"),
        ('{some} tricky/weird% (chars)', "some tricky weird% (chars)")
        ]
    f = texttidy.remove_punctuation
    run_test(f, tests)
    run_list_test(f, tests)


def test_replace_tokens():
    tests = [
        ('Hi world', "hello world"),
        ('hey earth', "hello world"),
        ('re re. re-bad (re). re - re! re-re. more mOre. regard re re1 1re! re-1 1-re.',
        'reg reg. re-bad (reg). reg - reg! re-re. more mOre. regard reg re1 1re! re-1 1-re.')
        ]
    vals = {
        "hello": ["hi", "hey"],
        "world": ["earth"],
        "reg": ["re"]
    }
    f = texttidy.replace_tokens
    run_test(f, tests, vals)
    run_list_test(f, tests, vals)


def test_strip_stopwords():

    stopwords = ['i', 'say', 'to', 'you']

    tests = [
        ("I say 'Hello world' to you", "Hello world' to you"),
        ("(1) I say 'Hello world' to you!", "Hello world' to you!"),
        ("1st I say 'Hello world' to you!", "Hello world' to you!"),
        ("¢ 1st I say 'Hello world' to you! ¢", "Hello world' to you! ¢")
        ]

    f = texttidy.strip_stopwords
    options = {"from_start": True, "from_end": False, "remove_numeric_tokens": True, "trim_punc": True}
    run_test(f, tests, stopwords, **options)
    run_list_test(f, tests, stopwords, **options)

    tests = [
        ("I say 'Hello world' to you", "I say 'Hello world"),
        ("(1) I say 'Hello world' to you!", "(1) I say 'Hello world"),
        ("1st I say 'Hello world' to you 2nd!", "1st I say 'Hello world"),
        ("¢ 1st I say 'Hello world' to you! ¢", "¢ 1st I say 'Hello world")
        ]

    f = texttidy.strip_stopwords
    options = {"from_start": False, "from_end": True, "remove_numeric_tokens": True, "trim_punc": True}
    run_test(f, tests, stopwords, **options)
    run_list_test(f, tests, stopwords, **options)

    tests = [
        ("I say 'Hello world' to you", "Hello world"),
        ("(1) I say 'Hello world' to you!", "Hello world"),
        ("I say to you!", ""),
        ("1st I say 'Hello world' to you 2nd!", "Hello world"),
        ("¢ 1st I say 'Hello world' to you! ¢", "Hello world")
        ]

    f = texttidy.strip_stopwords
    options = {"from_start": True, "from_end": True, "remove_numeric_tokens": True, "trim_punc": True}
    run_test(f, tests, stopwords, **options)
    run_list_test(f, tests, stopwords, **options)


def test_remove_duplicate_sentencestops():
    tests = [
        ('hello. world.', 'hello. world.'),
        ('hello.. world.', 'hello. world.'),
        ('hello. . world', 'hello. world'),
        ('hello... world', 'hello. world'),
        ('hello. . . . world.', 'hello. world.'),
        ('hello!! ?? . . world.', 'hello! ? . world.'),
        ('hello!!??.. world.', 'hello!?. world.')
    ]
    f = texttidy.remove_duplicate_sentencestops
    run_test(f, tests)
    run_list_test(f, tests)
