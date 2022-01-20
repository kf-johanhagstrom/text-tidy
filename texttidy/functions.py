
import json
import re
from functools import wraps

from texttidy import config


# Additional functions
# ====================
# prefixes
# remove stopwords (small med and large lists?)
# spelling corrections
# list all acronyms (utils)
# list all text between quotes e.g. "lorum ipsum"
# remove un-opened or un-closed brackets


def vectorize(func, *args, **kwargs):
    # Enable lists, Pandas Series, Numpy arrays
    @wraps(func) # Need this to preserve function signatures and docstrings
    def wrapper(x, *args, **kwargs):
        if isinstance(x, list):
            return [func(i, *args, **kwargs) for i in x]
        return func(x, *args, **kwargs)
    return wrapper


@vectorize
def single_space(text):
    """ replace multiple whitespaces with a single space. """
    rx = r"\s{2,}"
    text = re.sub(rx, " ", text)
    return text.strip()


@vectorize
def space_sentencestops(text, stop_chars=".;!?,:"):
    """ Space end of sentence punctuation marks e.g. Bad stop.Good stop. --> Bad stop. Good stop. And remove spaces before end marks e.g. Bad .Good --> Bad. Good."""
    # Add a single space after each stop character
    for c in stop_chars:
        rx = f"(\\{c}(?=[a-zA-Z]))"
        text = re.sub(rx, f"{c} ", text)

    # Remove the preceding space before a stop charater
    rx = fr"((?<=[a-zA-Z0-9])\s{{1,}}(?=[{stop_chars}]))"
    text = re.sub(rx, '', text)

    return text


@vectorize
def add_fullstop(text, stop_chars='.?!', replace_chars=';:,-/'):
    """ Add a fullstop to the end of a string if it does not exist """
    text = text.strip()
    if replace_chars is not None:
        if text[-1] in replace_chars:
            text = text[0:-1]
            return add_fullstop(text, stop_chars=stop_chars, replace_chars=replace_chars)
    if text[-1] not in stop_chars:
        text+='.'
    return text


@vectorize
def remove_numerical_commas(text):
    """ Remove commas from numerical numbers e.g. 1,000,000 --> 1000000 """
    rx = r"((?<=\d)\,(?=\d))"
    return re.sub(rx, "", text)


@vectorize
def remove_dashes(text):
    """ Remove dashes between acronym-styled words where the character preceding the dash is an upper-case letter and the character following the dash is either an upper-case letter or digit, e.g. COVID-19 --> COVID19. one-to-one --> one-to-one."""
    # Replace all long dashes with short dashes everywhere
    rx = r"\–"
    text = re.sub(rx, "-", text)

    # remove dashes between word and numbers
    rx = r"((?<=[A-Z])\-(?=[A-Z|\d]))"
    text = re.sub(rx, "", text)

    # remove dashes seperated by white spaces. incl long and short dashes
    rx = r"((?<=\s){1,}\-{1,}(?=\s){1,})"
    text = re.sub(rx, "", text)

    # space dashes that follow any non-whitespace and followed by a whitespace
    # eg hello- world --> hello world
    rx = r"((?<=[\S])\-(?=\s))"
    text = re.sub(rx, "", text)

    # Remove dashes at the start of a string
    rx = r"(^\-(?=\s){1,})"
    text = re.sub(rx, "", text)

    # Remove dashes that follow a sentence stop
    rx = r"((?<=[^a-zA-Z0-9])\-(?=[a-zA-Z|\d]))"
    text = re.sub(rx, " ", text)
    return text


@vectorize
def remove_bullets(text):
    """ Remove bullet characters and replace with fullstop. ●•·"""
    bullets = ['○', '●', '•', '·']
    s = "\\" + ("|\\").join(bullets)

    # Remove bullets at start of string and replace with space
    text = text.strip()

    rx = f"^({s})"
    text = re.sub(rx, ' ', text)

    # remove any other bullet and replace with fullstop
    rx = f"{s}"
    text = re.sub(rx, '.', text)

    text = text.strip()
    return space_sentencestops(text)


@vectorize
def replace_tokens(text, values):
    """ Replace tokens as specified in a passed dictionary {k: [v1, v2, v]} where tokens v in the text will be replaced by token k. """
    for k, v in values.items():
        for i in v:
            rx = rf"(^|(?<=[^\-]))(\b({i})\b)((?=[^\-])|$)"
            text = re.sub(rx, k, text, flags=re.IGNORECASE)

    return text


@vectorize
def remove_escapes(text):
    """ Remove escape characters and replace with fullstop except if the escape is at the start of a string. """
    escapes = ['\\n', '\\t', '\\r']
    text = text.strip()
    for escape in escapes:
        rx = f"^{escape}"
        text = re.sub(rx, ' ', text)

    for escape in escapes:
        rx = f"{escape}"
        text = re.sub(rx, '. ', text)

    text = text.strip()
    return space_sentencestops(text)


@vectorize
def replace_contractions(text):
    """ Replace common contractions (e.g. don't) with full form (e.g. do not). The list of contractions have been derived from wikipedia (see: List of English contractions)."""
    rx_compiled = []
    for k, v in config.CONTRACTIONS.items():
        s = k
        if k.lower() not in config.CONTRACTIONS_EXCEPTIONS:
            s1 = k.replace("'", "")
            s += f"|{s1}"

        # sub exact matches
        rx = re.compile(rf"((?<=\s)|^)({s})((?=\s)|$)", flags=re.IGNORECASE)
        rx_compiled.append((rx, v))

    for rx, rpl in rx_compiled:
        text = rx.sub(rpl, text)

    return text


@vectorize
def clean_quote_chars(text):
    """ Simplify usage of quotations and single apostraphies including (‘ ’ ´) and (“ ”) """
    rx = r"[‘’´]"
    text = re.sub(rx, "'", text)

    rx = r"[“”]"
    text = re.sub(rx, '"', text)
    return text


@vectorize
def replace_latin_abbrevs(text):
    """ Replace Latin abbreviations (eg, ie, and NB) with tidier forms (such as: (e.g.|e. g.|e.g) --> eg)"""
    rx = r"((?<=\s)|^)(e\.g\.|e\. g\.|e\.g)((?=\s)|$)"
    text = re.sub(rx, "eg", text, flags=re.IGNORECASE)

    rx = r"((?<=\s)|^)(i\.e\.|i\. e\.|i\.e)((?=\s)|$)"
    text = re.sub(rx, "ie", text, flags=re.IGNORECASE)

    rx = r"((?<=\s)|^)(n\.b\.|n\. b\.|n\.b)((?=\s)|$)"
    text = re.sub(rx, "nb", text, flags=re.IGNORECASE)
    return text


@vectorize
def remove_pronouns(text, pronouns='default'):
    """ Remove pronouns from text """
    if pronouns=='default':
        pronouns = config.PRONOUNS

    else:
        if not isinstance(pronouns, list):
            arg_type = type(pronouns)
            raise TypeError(f"pronouns arguement expecting a list but received {arg_type}")

    s = "|".join(pronouns)
    rx = re.compile(rf"\b({s})\b", flags=re.IGNORECASE)
    text = rx.sub('', text)

    return single_space(text)


@vectorize
def remove_punctuation(text, remove='all', keep='.,?!()%&'):
    """Remove all punctuation except those marked keep

    Args:
        text (str or list): text or list of strings to clean.
        remove (str, optional): If "all" then uses the default characters in texttidy.PUNCT_ALL, else removes all characters in the string. Defaults to 'all'.
        keep (str, optional): Keeps all characters in the string. Defaults to '.,?!()%&'.
    """
    if remove=='all':
        remove = config.PUNCT_ALL


    chars = ''
    for c in remove:
        if not c in keep:
            chars+=c

    for c in chars:
        rx = f"(\\{c})"
        text = re.sub(rx, " ", text)

    return single_space(text)


@vectorize
def strip_stopwords(text, stopwords, from_start=True, from_end=True, remove_numeric_tokens=False, trim_punc=True):
    """Remove stopwords from text string.

    Args:
        text (str or list): text to be cleaned.
        stopwords (list): list of stopwords to be removed
        from_start (bool, optional): Remove only stopwords from the start of text - continue until a non-stopword is found. Defaults to True.
        from_end (bool, optional): Remove only stopwords from the end of text - continue until a non-stopword is found. Defaults to True.
        remove_numeric_tokens (bool, optional): Remove any token that contains one or more digits from the start or end.
        trim_punc (bool, optional): remove any punctuation encountered.

    Returns:
        str or list: cleaned text.
    """

    if text=="":
        return text

    re_hasdigits = re.compile(r"\d")

    if from_start:
        if trim_punc:
            # Dont use built in punct and check for non-alphanumeric chars instead.
            if not text[0].isalnum():
                text = text[1:].strip()
                return strip_stopwords(text, stopwords, from_start=from_start, from_end=from_end, remove_numeric_tokens=remove_numeric_tokens, trim_punc=trim_punc)

        rx = r"^([\w\-]+)"
        match = re.findall(rx, text)[0]

        if remove_numeric_tokens:
            if re_hasdigits.search(match) is not None:
                text = text.replace(match, "", 1).strip()
                return strip_stopwords(text, stopwords, from_start=from_start, from_end=from_end, remove_numeric_tokens=remove_numeric_tokens, trim_punc=trim_punc)

        if match.lower() in stopwords:
            text = text.replace(match, "", 1).strip()
            return strip_stopwords(text, stopwords, from_start=from_start, from_end=from_end, remove_numeric_tokens=remove_numeric_tokens, trim_punc=trim_punc)

    if from_end:
        if trim_punc:
            # Dont use built in punct and check for non-alphanumeric chars instead.
            if not text[-1].isalnum():
                text = text[:-1].strip()
                return strip_stopwords(text, stopwords, from_start=from_start, from_end=from_end, remove_numeric_tokens=remove_numeric_tokens, trim_punc=trim_punc)

        rx = r"([\w\-]+)$"
        rx_match = re.finditer(rx, text)
        match, idx = [(x.group(0), x.start()) for x in rx_match][0]

        if remove_numeric_tokens:
            if re_hasdigits.search(match) is not None:
                text = text.replace(match, "", 1).strip()
                return strip_stopwords(text, stopwords, from_start=from_start, from_end=from_end, remove_numeric_tokens=remove_numeric_tokens, trim_punc=trim_punc)

        if match.lower() in stopwords:
            text = text[:idx].strip()
            return strip_stopwords(text, stopwords, from_start=from_start, from_end=from_end, remove_numeric_tokens=remove_numeric_tokens, trim_punc=trim_punc)

    return text


@vectorize
def remove_duplicate_sentencestops(text, stop_chars=".;!?:"):
    """Remove duplicate sentence stops eg hello world... --> hello world.

    Args:
        text (str or list): text to be cleaned.
        stop_chars (str, optional): Sentence stop characters to check for duplicates. Defaults to ".;!?:".
    """
    # First remove spaces between duplicates stop characters
    # eg hello . . world --> hello .. world
    for c in stop_chars:
        rx = f"(?<=\\{c})\s(?=\\{c})"
        text = re.sub(rx, "", text)

    # Then remove duplicates (if 2 or more consequtive)
    for c in stop_chars:
        rx = f"\\{c}{{2,}}"
        text = re.sub(rx, f"{c}", text)
    return text
