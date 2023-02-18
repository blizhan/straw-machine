from sklearn.base import BaseEstimator, TransformerMixin

from typing import Callable, List, List, Dict
from dataclasses import dataclass


@dataclass
class operator:
    name: str
    func: Callable
    inputs: List[str]
    outputs: List[str]
    kw_args: Dict[str, object]=None

class estimator(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        oper: operator
    ):
        self.oper = oper
        self.name = oper.name
        self.inputs = oper.inputs
        self.validate = False
        pass

    @staticmethod
    def enabled(**kwargs):
        return True

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if self.oper.kw_args is not None:
            X = self.oper.func(X[self.oper.inputs], **self.oper.kw_args)
        else:
            X = self.oper.func(X)
        return X[self.oper.outputs]

    def get_feature_names_out(self, name):
        return self.oper.outputs

def generate_estimator(
        name: str,
        func: Callable,
        inputs: List[str],
        outputs: List[str],
        kw_args: Dict[str, object]=None
    ) -> estimator:

    oper = operator(
        name=name,
        func=func,
        inputs=inputs,
        outputs=outputs,
        kw_args=kw_args
    )
    e = estimator(oper)
    return e
