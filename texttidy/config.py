
import importlib.resources
import json

import texttidy

from . import data


def load_contractions():
    with importlib.resources.open_text(data, "common_contractions.json") as file:
        return json.load(file)


def load_contraction_exceptions():
    with importlib.resources.open_text(data, "common_contractions_exceptions.txt") as file:
        return file.read().split()


def load_pronouns():
    with importlib.resources.open_text(data, "pronouns.txt") as file:
        return file.read().split()


def load_fullmonty_pipeline():
    with importlib.resources.open_text(data, "fullmonty.json") as file:
        return json.load(file)


CONTRACTIONS = load_contractions()
CONTRACTIONS_EXCEPTIONS = load_contraction_exceptions()
PRONOUNS = load_pronouns()

PUNCT_ALL = '!"#$£€%&\'()*+,-./:;<=>?@[\\]^_`{|}~©™•_”~[]¦¬¿●·±®○«»°，'

# Pipeline
FULLMONTY = load_fullmonty_pipeline()
