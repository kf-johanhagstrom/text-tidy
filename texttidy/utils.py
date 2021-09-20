""" pkg utility functions """

import inspect
import json

import texttidy


def generate_pipeline_file(steps, write_to_json=None):
    """Generate a pipeline dictionary and json file based on the list of steps provided.

    Args:
        steps (list): List of fucntion steps given as strings.
        write_to_json (None or str, optional): Filepath to save the pipeline as a json file. If None, no file is written. Defaults to None.

    Returns:
        dict: Pipeline as a dictionary.
    """

    eval_steps = []
    for step in steps:
        try:
            eval_steps.append(eval(f"texttidy.{step}"))
        except:
            raise TypeError(f"'{step}' not recognised in function list.")

    output = {}
    for i, f in enumerate(eval_steps):
        sig = inspect.signature(f)

        kwargs = {}
        for p in sig.parameters.values():
            arg = p.name
            val = p.default
            if val is not p.empty:
                kwargs[arg] = val

        output[str(i)] = {
            "step": f.__name__,
            "kwargs": kwargs
        }

    if write_to_json is not None:
        json.dump(output, open(write_to_json, 'w'))

    return output
