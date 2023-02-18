from straw_machine.dataclass import estimator, operator, transformer, step, pipeline

from sklearn.pipeline import Pipeline

from typing import Callable, List, Dict

def generate_estimator(
        name: str,
        func: Callable,
        inputs: List[str],
        outputs: List[str],
        kw_args: Dict[str, object]=None,
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

def generate_transformer(
    name:str,
    estimators: List[estimator],
    **kwargs,
) -> transformer:

    s = step(
        name=name,
        estimators=estimators
    )
    return transformer(s, **kwargs)


def generate_pipeline(
    transformers: List[transformer],
    **kwargs
)->Pipeline:
    """_summary_

    Args:
        name (str): _description_
        transformers (List[transformer]): _description_

    Returns:
        Pipeline: _description_
    """

    steps = [(t.name, t) for t in transformers]
    pl = pipeline(steps=steps, **kwargs)
    pl.set_output()
    return pl