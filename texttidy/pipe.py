
import inspect
import json

from tqdm import tqdm

import textstada


class Pipeline:
    def __init__(self, text=None, pipe=None, verbose=False):
        self.pipe = pipe
        self.text_input = text
        self.steps = None
        self._kwargs = None
        self._get_steps_params()
        self._steps = self._evaluate_steps()
        self._verbose = verbose
        self.text_output = None


    def _get_steps_params(self):
        steps = []
        kwargs = []
        for k, v in self.pipe.items():
            step = v.get('step')
            kwarg = v.get('kwargs', {})

            if step is None:
                raise ValueError(f"Function not defined in step: ({k}).")

            steps.append(v['step'])
            kwargs.append(kwarg)

        self.steps = steps
        self._kwargs = kwargs


    def _evaluate_steps(self):
        eval_steps = []
        for step in self.steps:
            try:
                eval_steps.append(eval(f"textstada.{step}"))
            except:
                raise TypeError(f"'{step}' not recognised in function list.")
        return eval_steps


    def _run_func(self, t, func, *args, **kwargs):
        return func(t, *args, **kwargs)


    def run(self):
        t = self.text_input

        if t is None:
            raise ValueError("Please add text to 'self.text_input' before running pipe.")

        funcs = zip(self._steps, self._kwargs)

        for step, kwarg in tqdm(funcs, disable=not self._verbose):
            t = self._run_func(t, step, **kwarg)

        self.text_output = t
