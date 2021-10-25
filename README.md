# Text Tidy
No frills curated text data cleaning methods for common text pre-processing in the NLP workflow.

## Intro
Text mining and NLP tasks and workflows is predicated by - sometimes - considerable text cleaning operations.

I found that, although the concept behind such operations like removing, fixing or replacing words and characters may be easy, the implementation quickly becomes cumbersome especially when trying to account for the endless different possibilities and subtleties that come with language. I also found that the number of functions to do all this text tidying quickly becomes overwhelming, diverting your attention away from the actually mining you wanted to do in the first place.

Furthermore, if you're playing with NLP workflows or machine learning, the steps taken to clean the text used for training purposes should mirror any new text that you feed to the model. This leads to doubling up of lots of functions and processes, and more code to keep track of.

This package tries to simplify the text pre-processing steps. A curated list of reusable text cleaning functions can do the majority of text cleaning tasks for you. A pipeline also lets you construct a sequence of text cleaning functions that can be reused throughout your NLP workflow.


## Quick start

Make use of individual text cleaning functions.

```python
import texttidy

text = " This   sentences is riddled with 'formatting' mistakes, characters and punctuation, which (needs) fixing before we're able to do any  further NLP tasks ..  - This is where texttidy can help"

text = texttidy.single_space(text)
text = texttidy.remove_dashes(text)
text = texttidy.remove_duplicate_sentencestops(text)
text = texttidy.space_sentencestops(text)
text = texttidy.replace_contractions(text)
text = texttidy.add_fullstop(text)
text = texttidy.remove_punctuation(text)

>>> 'This sentences is riddled with formatting mistakes, characters and punctuation, which (needs) fixing before we are able to do any further NLP tasks. This is where texttidy can help.'
```

Or use the pipeline to clean text using the sequence of functions.

```python
import texttidy
from texttidy import Pipeline

text = " This   sentences is riddled with 'formatting' mistakes, characters and punctuation, which (needs) fixing before we're able to do any  further NLP tasks ..  - This is where texttidy can help"

steps = [
    'single_space',
    'remove_dashes',
    'remove_duplicate_sentencestops',
    'space_sentencestops',
    'replace_contractions',
    'add_fullstop',
    'remove_punctuation'
]

pipeline = texttidy.utils.generate_pipeline_file(steps)
pipe = Pipeline(text=text, pipe=pipeline)
pipe.run()
pipe.text_output

>>> 'This sentences is riddled with formatting mistakes, characters and punctuation, which (needs) fixing before we are able to do any further NLP tasks. This is where texttidy can help.'
```
