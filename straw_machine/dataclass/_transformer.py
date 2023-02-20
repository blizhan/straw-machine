from straw_machine.dataclass import estimator

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import cloudpickle

from dataclasses import dataclass
from typing import List
import os

@dataclass
class step:
    name: str
    estimators: List[estimator]

class pipeline(Pipeline):
    def __init__(self, steps, *, memory=None, verbose=False):
        super().__init__(steps, memory=memory, verbose=verbose)

    def __add__(self, pl) -> Pipeline:
        steps = self.steps.copy()
        if isinstance(pl, transformer):
            steps.append((pl.name, pl))
        elif isinstance(pl, Pipeline) or isinstance(pl, pipeline):
            steps.extend(pl.steps)
        return pipeline(steps)

    def save(self, savepath, **kwargs):
        dir = os.path.dirname(savepath)
        if len(dir):
            os.makedirs(dir, exist_ok=True)
        with open(savepath, 'wb') as f:
            cloudpickle.dump(self, f, **kwargs)


class transformer(ColumnTransformer):
    def __init__(self, transform_step:step, **kwargs):
        self.name = transform_step.name
        self.transform_step = step
        self.cols_tranform_list = [(e.name, e, e.inputs) for e in transform_step.estimators]

        super().__init__(
            transformers=self.cols_tranform_list,
            remainder='passthrough',
            verbose_feature_names_out=False,
            # **kwargs
        )
        super().set_output(transform='pandas')

    def save(self, savepath, **kwargs):
        dir = os.path.dirname(savepath)
        if len(dir):
            os.makedirs(dir, exist_ok=True)
        with open(savepath, 'wb') as f:
            cloudpickle.dump(self, f, **kwargs)

    def __add__(self, trans) -> pipeline:
        if isinstance(trans, transformer):
            steps = [(self.name, self), (trans.name, trans)]
        elif isinstance(trans, pipeline) or isinstance(trans, Pipeline):
            steps = [(self.name, self)]
            steps.extend(trans.steps)
        pl = pipeline(steps=steps)
        return pl

    def rename(self, name:str):
        self.name = name
        return self
