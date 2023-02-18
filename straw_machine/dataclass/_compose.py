from straw_machine.dataclass import estimator

from sklearn.base import TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.utils.metaestimators import _BaseComposition

from dataclasses import dataclass
from typing import List

@dataclass
class step:
    name: str
    estimators: List[estimator]

class compose(ColumnTransformer):
    def __init__(self, compose_step:step, **kwargs):
        self.name = compose_step.name
        self.compose_step = step
        self.cols_tranform_list = [(e.name, e, e.inputs) for e in compose_step.estimators]

        super().__init__(
            transformers=self.cols_tranform_list,
            remainder='passthroght',
            verbose_feature_names_out=False,
            **kwargs
        )
        super().set_output(transform='pandas')

    def get_step(self):
        pass

def generate_compose(
    name:str,
    estimators: List[estimator],
    **kwargs,
) -> compose:

    s = step(
        name=name,
        estimators=estimators
    )
    compose(s, **kwargs)
    return
