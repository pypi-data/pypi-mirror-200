import base64
import pickle
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd
from pydantic import BaseModel


def encode_data(data: pd.DataFrame) -> str:
    pickled = pickle.dumps(data)
    pickled_b64 = base64.b64encode(pickled)
    pickled_str = pickled_b64.decode("utf-8")
    return pickled_str


def decode_data(encoded_data: str) -> pd.DataFrame:
    return pickle.loads(base64.b64decode(encoded_data.encode()))


class Data(BaseModel):  # type: ignore
    name: str
    description: Optional[str] = None
    dataset: str  # encoded dataset
    features: Optional[List[str]]  # column names
    target: str
    split: Optional[float] = 0.25
    balance: Optional[float] = 0
    max_depth: Optional[int] = 10  # create restriction from 1-32
    control_class: Optional[str | int]  # class to be used to generate metrics
    model_id: Optional[int]


class APIKeyRequest(BaseModel):
    name: str
    expires: int


class RuleEvalRequest(BaseModel):
    raw_rule: Optional[str]
    rule_id: Optional[str]
    datapoint: str


class PredictRequest(BaseModel):
    model_id: int | str
    datapoint: str


@dataclass
class Prediction:
    datapoint: pd.DataFrame
    result: Any
    confidence: Dict[str, float]


@dataclass
class Rules:
    rule_set: pd.DataFrame
    importance: pd.DataFrame  # each feature + their relevance score


@dataclass
class FeatureImportance:
    table: pd.DataFrame
