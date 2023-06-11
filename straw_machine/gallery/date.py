from straw_machine.util import generate_estimator, generate_transformer

from datetime import datetime
import math

import pandas as pd

date_col_pattern = '{incol}-{item}'

def date2sinhour(df:pd.DataFrame, incol:str, outcol:str) -> pd.DataFrame:
    df[outcol] = df[incol].dt.hour.apply(lambda x : math.sin(x/24))
    return df

def date2coshour(df:pd.DataFrame, incol:str, outcol:str) -> pd.DataFrame:
    df[outcol] = df[incol].dt.hour.apply(lambda x : math.cos(x/24))
    return df

def date2sinmonth(df:pd.DataFrame, incol:str, outcol:str) -> pd.DataFrame:
    df[outcol] = df[incol].dt.month.apply(lambda x : math.sin((x-1)/12))
    return df

def date2cosmonth(df:pd.DataFrame, incol:str, outcol:str) -> pd.DataFrame:
    df[outcol] = df[incol].dt.month.apply(lambda x : math.cos((x-1)/12))
    return df

def date2sinweekday(df:pd.DataFrame, incol:str, outcol:str) -> pd.DataFrame:
    df[outcol] = df[incol].dt.weekday.apply(lambda x : math.sin(x/7))
    return df

def date2cosweekday(df:pd.DataFrame, incol:str, outcol:str) -> pd.DataFrame:
    df[outcol] = df[incol].dt.weekday.apply(lambda x : math.cos(x/7))
    return df


date_normalize_items = {
    'sinhour': date2sinhour,
    'coshour': date2coshour,
    'sinmonth': date2sinmonth,
    'cosmonth': date2cosmonth,
    'sinweekday': date2sinweekday,
    'cosweekday': date2cosweekday,
}


def generate_date_normalize_transformer(incol:str):
    """generate date normalize_transformer

    Args:
        incol (str): input date columns

    Returns:
        _type_: _description_
    """
    date_estimators = []

    for k,v in date_normalize_items.items():
        outs = [incol, date_col_pattern.format(incol=incol, item=k)] if len(date_estimators)==0 else date_col_pattern.format(incol=incol, item=k)
        e = generate_estimator(
            name=date_col_pattern.format(incol=incol, item=k),
            func=v,
            inputs=[incol],
            outputs=outs,
            kw_args={
                'incol': incol,
                'outcol': date_col_pattern.format(incol=incol, item=k)
            }
        )
        date_estimators.append(e)

    date_transformer = generate_transformer(
        name=date_col_pattern.format(incol=incol, item='date_transforn'),
        estimators=date_estimators,
        remain_other=True
    )
    return date_transformer
